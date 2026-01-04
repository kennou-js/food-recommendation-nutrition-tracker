from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from models.food import FoodDatabase
from models.user import UserManager
from utils.chatbot import NutritionChatbot
from utils.calculator import NutritionCalculator
from datetime import datetime, date
import os
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = 'food_tracker_secret_key_development'

# Initialize data directory
os.makedirs('data', exist_ok=True)

# Initialize components
food_db = FoodDatabase('data/food_database.csv')
user_manager = UserManager('data/users.json')
chatbot = NutritionChatbot(food_db, user_manager)
calculator = NutritionCalculator()

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Login page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            # Simple authentication
            user_id = f"user_{hash(username) % 1000000}"
            
            # Check if user exists
            user_profile = user_manager.get_user(user_id)
            
            if user_profile:
                # User exists, log them in
                session['user_id'] = user_id
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                # New user - create basic entry and redirect to profile setup
                session['user_id'] = user_id
                session['username'] = username
                return redirect(url_for('profile_setup'))
        else:
            return render_template('login.html', error='Please enter username and password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """Registration page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
            return render_template('register.html', error="All fields are required")
        
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")
        
        if len(password) < 6:
            return render_template('register.html', error="Password must be at least 6 characters")
        
        # Create user ID
        user_id = f"user_{hash(username + email) % 1000000}"
        
        # Check if user already exists
        if user_manager.get_user(user_id):
            return render_template('register.html', error="User already exists")
        
        # Store basic user info in session (but don't create full profile yet)
        session['user_id'] = user_id
        session['username'] = username
        
        # Store basic info that will be used in profile setup
        session['temp_user'] = {
            'username': username,
            'email': email
        }
        
        # Redirect to profile setup
        return redirect(url_for('profile_setup'))
    
    return render_template('register.html')
@app.route('/api/initial_profile', methods=['POST'])
def create_initial_profile():
    """Create initial user profile after registration"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    user_id = session['user_id']
    
    try:
        user_data = user_manager.create_user(
            user_id=user_id,
            name=data.get('name', 'User'),
            age=int(data.get('age', 30)),
            weight=float(data.get('weight', 70)),
            height=float(data.get('height', 175)),
            gender=data.get('gender', 'male'),
            activity_level=data.get('activity_level', 'moderate'),
            goal=data.get('goal', 'maintain')
        )
        
        bmi = calculator.calculate_bmi(float(data.get('weight', 70)), float(data.get('height', 175)))
        bmi_category = calculator.bmi_category(bmi)
        water_intake = calculator.water_intake_recommendation(float(data.get('weight', 70)), data.get('activity_level', 'moderate'))
        
        user_data['bmi'] = round(bmi, 1)
        user_data['bmi_category'] = bmi_category
        user_data['water_intake'] = round(water_intake, 2)
        
        return jsonify(user_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/profile-setup', methods=['GET', 'POST'])
def profile_setup():
    """Profile setup page for new users"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        # Process profile setup form
        name = request.form.get('name')
        age = request.form.get('age')
        weight = request.form.get('weight')
        height = request.form.get('height')
        gender = request.form.get('gender')
        activity_level = request.form.get('activity_level')
        goal = request.form.get('goal')
        
        if all([name, age, weight, height, gender, activity_level, goal]):
            # Create user profile with actual data
            user_data = user_manager.create_user(
                user_id=user_id,
                name=name,
                age=int(age),
                weight=float(weight),
                height=float(height),
                gender=gender,
                activity_level=activity_level,
                goal=goal
            )
            
            return redirect(url_for('dashboard'))
    
    # Check if user already has a profile
    user_profile = user_manager.get_user(user_id)
    if user_profile and 'name' in user_profile:
        return redirect(url_for('dashboard'))
    
    return render_template('profile_setup.html')

@app.route('/')
def dashboard():
    """Main dashboard page - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    user_id = session.get('user_id')
    user_profile = user_manager.get_user(user_id)
    
    return render_template('index.html', user_profile=user_profile)

@app.route('/profile')
def profile_page():
    """User profile management page - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    user_id = session.get('user_id')
    user_profile = user_manager.get_user(user_id)
    return render_template('profile.html', user_profile=user_profile)

@app.route('/chatbot')
def chatbot_page():
    """Nutrition assistant chatbot page - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('chatbot.html')

@app.route('/food-log')
def food_log_page():
    """Food logging and tracking page - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    user_id = session.get('user_id')
    user_profile = user_manager.get_user(user_id)
    return render_template('foodlog.html', user_profile=user_profile)

@app.route('/recommendations')
def recommendations_page():
    """Food recommendations page - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('recommendations.html')

@app.route('/database')
def database_page():
    """Database management page - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('database.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/search', methods=['GET'])
def search_food():
    """Search food - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    query = request.args.get('q', '')
    print(f"DEBUG: Searching for food: '{query}'")
    
    if query:
        try:
            results = food_db.search_food(query, top_n=10)
            print(f"DEBUG: Found {len(results)} results")
            for i, result in enumerate(results):
                print(f"DEBUG: Result {i}: {result}")
            return jsonify(results)
        except Exception as e:
            print(f"DEBUG: Search error: {str(e)}")
            return jsonify({'error': str(e)}), 500
    return jsonify([])

@app.route('/api/recommend', methods=['GET'])
def recommend_food():
    """Recommend food - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    food_name = request.args.get('food', '')
    if food_name:
        try:
            recommendations = food_db.get_recommendations(food_name)
            return jsonify(recommendations)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify([])

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with assistant - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    message = data.get('message', '')
    user_id = session.get('user_id', 'anonymous')
    
    try:
        response = chatbot.process_message(message, user_id)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create_user', methods=['POST'])
def create_user():
    """Create/update user profile - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    user_id = session['user_id']
    
    try:
        user_data = user_manager.create_user(
            user_id=user_id,
            name=data.get('name', 'User'),
            age=int(data.get('age', 30)),
            weight=float(data.get('weight', 70)),
            height=float(data.get('height', 175)),
            gender=data.get('gender', 'male'),
            activity_level=data.get('activity_level', 'moderate'),
            goal=data.get('goal', 'maintain')
        )
        
        bmi = calculator.calculate_bmi(float(data.get('weight', 70)), float(data.get('height', 175)))
        bmi_category = calculator.bmi_category(bmi)
        water_intake = calculator.water_intake_recommendation(float(data.get('weight', 70)), data.get('activity_level', 'moderate'))
        
        user_data['bmi'] = round(bmi, 1)
        user_data['bmi_category'] = bmi_category
        user_data['water_intake'] = round(water_intake, 2)
        
        return jsonify(user_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    """Update existing user profile - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401
    
    try:
        updated_data = user_manager.update_user(
            user_id=user_id,
            name=data.get('name'),
            age=int(data.get('age')) if data.get('age') else None,
            weight=float(data.get('weight')) if data.get('weight') else None,
            height=float(data.get('height')) if data.get('height') else None,
            gender=data.get('gender'),
            activity_level=data.get('activity_level'),
            goal=data.get('goal')
        )
        
        if updated_data:
            return jsonify(updated_data)
        return jsonify({'error': 'Failed to update profile'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/remove_food', methods=['POST'])
def remove_food():
    """Remove specific food entry - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    user_id = session.get('user_id')
    log_date = data.get('date')
    food_name = data.get('food_name')
    quantity = data.get('quantity')
    
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401
    
    if not log_date or not food_name:
        return jsonify({'error': 'Date and food name are required'}), 400
    
    try:
        # Get the user's daily logs
        user_data = user_manager.get_user(user_id)
        if not user_data or 'daily_logs' not in user_data:
            return jsonify({'error': 'No food logs found'}), 404
        
        if log_date in user_data['daily_logs']:
            logs = user_data['daily_logs'][log_date]
            original_count = len(logs)
            
            # Filter out the matching entries
            filtered_logs = []
            removed_count = 0
            
            for log in logs:
                if log['food'] == food_name:
                    if quantity is None or log['quantity'] == float(quantity):
                        removed_count += 1
                        continue
                filtered_logs.append(log)
            
            # Update the logs
            if filtered_logs:
                user_data['daily_logs'][log_date] = filtered_logs
            else:
                del user_data['daily_logs'][log_date]
            
            # Save changes
            user_manager._save_users()
            
            return jsonify({
                'status': 'success',
                'message': f'Removed {removed_count} entry(ies) for {food_name}',
                'removed_count': removed_count,
                'logs': filtered_logs
            })
        else:
            return jsonify({'error': 'No food logs found for this date'}), 404
    except Exception as e:
        print(f"DEBUG: Exception in remove_food: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear_daily_logs', methods=['POST'])
def clear_daily_logs():
    """Clear daily logs - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401
    
    log_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    try:
        user_data = user_manager.get_user(user_id)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        if 'daily_logs' in user_data and log_date in user_data['daily_logs']:
            # Count how many logs are being cleared
            logs_cleared = len(user_data['daily_logs'][log_date])
            
            # Clear the logs
            del user_data['daily_logs'][log_date]
            user_manager._save_users()
            
            return jsonify({
                'status': 'success',
                'message': f'Cleared {logs_cleared} food log(s) for {log_date}',
                'logs_cleared': logs_cleared
            })
        else:
            return jsonify({
                'status': 'success',
                'message': f'No logs found for {log_date}',
                'logs_cleared': 0
            })
    except Exception as e:
        print(f"DEBUG: Exception in clear_daily_logs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/daily_summary', methods=['GET'])
def daily_summary():
    """Get daily summary - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session.get('user_id')
    log_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    print(f"DEBUG: Getting daily summary for user {user_id} on date {log_date}")
    
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401
    
    try:
        # Get user profile
        user_profile = user_manager.get_user(user_id)
        print(f"DEBUG: User profile found: {user_profile is not None}")
        
        # Get daily logs
        logs = user_manager.get_daily_summary(user_id, log_date)
        print(f"DEBUG: Daily logs: {logs}")
        
        # Calculate nutrition totals
        nutrition_totals = {
            'calories': 0,
            'protein': 0,
            'fat': 0,
            'carbs': 0,
            'fiber': 0,
            'sugar': 0
        }
        
        if logs:
            print(f"DEBUG: Calculating nutrition for {len(logs)} logs")
            # Convert logs to food list for calculation
            food_list = []
            for log in logs:
                food_list.append({
                    'name': log['food'],
                    'quantity': log['quantity']
                })
            
            # Calculate nutrition
            try:
                calculated_nutrition = food_db.calculate_nutrition(food_list)
                nutrition_totals.update(calculated_nutrition)
                print(f"DEBUG: Calculated nutrition: {calculated_nutrition}")
            except Exception as e:
                print(f"Nutrition calculation error: {e}")
        
        # Add target calories if user profile exists
        if user_profile:
            nutrition_totals['target_calories'] = user_profile.get('daily_calories', 2000)
            # Calculate calorie status
            if 'calories' in nutrition_totals:
                calorie_diff = nutrition_totals['calories'] - nutrition_totals['target_calories']
                if calorie_diff > 500:
                    nutrition_totals['calorie_status'] = 'high_surplus'
                elif calorie_diff > 0:
                    nutrition_totals['calorie_status'] = 'surplus'
                elif calorie_diff < -500:
                    nutrition_totals['calorie_status'] = 'high_deficit'
                elif calorie_diff < 0:
                    nutrition_totals['calorie_status'] = 'deficit'
                else:
                    nutrition_totals['calorie_status'] = 'maintenance'
        
        return jsonify({
            'logs': logs if logs else [],
            'nutrition': nutrition_totals,
            'user_profile': user_profile
        })
    except Exception as e:
        print(f"DEBUG: Exception in daily_summary: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/all_foods', methods=['GET'])
def get_all_foods():
    """Get all foods - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        df = pd.read_csv('data/food_database.csv')
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_food', methods=['POST'])
def add_food():
    """Add food to database - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    
    try:
        # Read existing database
        df = pd.read_csv('data/food_database.csv')
        
        # Create new food entry
        new_id = int(df['id'].max()) + 1 if len(df) > 0 else 1
        new_food = {
            'id': new_id,
            'name': data['name'],
            'category': data.get('category', 'Other'),
            'calories': float(data['calories']),
            'protein': float(data.get('protein', 0)),
            'fat': float(data.get('fat', 0)),
            'carbs': float(data.get('carbs', 0)),
            'fiber': float(data.get('fiber', 0)),
            'sugar': float(data.get('sugar', 0))
        }
        
        # Add to dataframe
        df = pd.concat([df, pd.DataFrame([new_food])], ignore_index=True)
        
        # Save to CSV
        df.to_csv('data/food_database.csv', index=False)
        
        # Reload food database
        global food_db
        food_db = FoodDatabase('data/food_database.csv')
        
        return jsonify({'status': 'success', 'food': new_food})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/calculate_nutrition', methods=['POST'])
def calculate_nutrition():
    """Calculate nutrition - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    foods = data.get('foods', [])
    
    try:
        nutrition_totals = food_db.calculate_nutrition(foods)
        return jsonify(nutrition_totals)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clean_database', methods=['POST'])
def clean_database():
    """Clean database - requires login"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        df = pd.read_csv('data/food_database.csv')
        initial_count = len(df)
        
        # Filter out unrealistic entries
        df = df[~(
            (df['calories'] > 5000) |
            (df['protein'] > 100) |
            (df['fat'] > 100) |
            (df['carbs'] > 500)
        )]
        
        # Reset IDs
        df['id'] = range(1, len(df) + 1)
        
        # Save cleaned database
        df.to_csv('data/food_database.csv', index=False)
        
        # Reload food database
        global food_db
        food_db = FoodDatabase('data/food_database.csv')
        
        removed_count = initial_count - len(df)
        
        return jsonify({
            'status': 'success',
            'message': f'Cleaned database. Removed {removed_count} erroneous entries.',
            'food_count': len(df),
            'removed': removed_count
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error cleaning database: {str(e)}'
        }), 500

@app.route('/api/log_food', methods=['POST'])
def log_food():
    """Log food - requires login"""
    if 'user_id' not in session:
        print("DEBUG: No user_id in session - Authentication failed")
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    user_id = session.get('user_id')
    
    print(f"DEBUG: Received log_food request from user {user_id}: {data}")
    
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401
    
    try:
        # Get required fields
        food_name = data.get('food_name', '').strip()
        quantity = data.get('quantity', 1)
        log_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        print(f"DEBUG: Parsed - Food: '{food_name}', Quantity: {quantity}, Date: {log_date}")
        
        if not food_name:
            print("DEBUG: Food name is empty!")
            return jsonify({'error': 'Food name is required'}), 400
        
        # Clean the food name for search
        search_name = food_name
        
        # Check if food exists in database (case-insensitive)
        food_results = food_db.search_food(search_name, top_n=1)
        print(f"DEBUG: Food search results: {food_results}")
        
        exact_food_name = food_name  # Default to what was entered
        
        if not food_results:
            # Try fuzzy matching by checking if any food contains the entered name
            df = pd.read_csv('data/food_database.csv')
            # Find foods where the entered name is a substring (case-insensitive)
            matches = df[df['name'].str.contains(food_name, case=False, na=False)]
            if not matches.empty:
                # Use the first match's exact name
                exact_food_name = matches.iloc[0]['name']
                print(f"DEBUG: Found fuzzy match: '{exact_food_name}'")
            else:
                print(f"DEBUG: No matches found for '{food_name}'")
                return jsonify({'error': f'Food "{food_name}" not found in database'}), 404
        else:
            # Use the exact name from database
            exact_food_name = food_results[0]['name']
            print(f"DEBUG: Using exact name from database: '{exact_food_name}'")
        
        success = user_manager.add_food_log(
            user_id=user_id,
            date=log_date,
            food_name=exact_food_name,
            quantity=float(quantity),
            meal_type=data.get('meal_type'),
            timestamp=data.get('timestamp')
        )
        
        print(f"DEBUG: Log success: {success}")
        
        if success:
            # Get updated user data
            user_data = user_manager.get_user(user_id)
            logs = user_manager.get_daily_summary(user_id, log_date)
            
            return jsonify({
                'status': 'success',
                'message': f'Logged {quantity} serving(s) of {exact_food_name}',
                'food': exact_food_name,
                'quantity': quantity,
                'logs': logs if logs else []
            })
        return jsonify({'error': 'Failed to log food'}), 400
    except Exception as e:
        print(f"DEBUG: Exception in log_food: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
       

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'authenticated': 'user_id' in session
    })

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Create a sample food database if it doesn't exist
    food_db_path = 'data/food_database.csv'
    if not os.path.exists(food_db_path):
        sample_foods = [
            {'id': 1, 'name': 'Apple', 'category': 'Fruit', 'calories': 52, 'protein': 0.3, 'fat': 0.2, 'carbs': 14, 'fiber': 2.4, 'sugar': 10},
            {'id': 2, 'name': 'Banana', 'category': 'Fruit', 'calories': 89, 'protein': 1.1, 'fat': 0.3, 'carbs': 23, 'fiber': 2.6, 'sugar': 12},
            {'id': 3, 'name': 'Chicken Breast', 'category': 'Meat', 'calories': 165, 'protein': 31, 'fat': 3.6, 'carbs': 0, 'fiber': 0, 'sugar': 0},
            {'id': 4, 'name': 'White Rice', 'category': 'Grains', 'calories': 130, 'protein': 2.7, 'fat': 0.3, 'carbs': 28, 'fiber': 0.4, 'sugar': 0.1},
            {'id': 5, 'name': 'Eggs', 'category': 'Dairy & Eggs', 'calories': 155, 'protein': 13, 'fat': 11, 'carbs': 1.1, 'fiber': 0, 'sugar': 1.1},
            {'id': 6, 'name': 'Broccoli', 'category': 'Vegetables', 'calories': 34, 'protein': 2.8, 'fat': 0.4, 'carbs': 7, 'fiber': 2.6, 'sugar': 1.7},
            {'id': 7, 'name': 'Salmon', 'category': 'Fish', 'calories': 208, 'protein': 20, 'fat': 13, 'carbs': 0, 'fiber': 0, 'sugar': 0},
            {'id': 8, 'name': 'Bread', 'category': 'Grains', 'calories': 265, 'protein': 9, 'fat': 3.2, 'carbs': 49, 'fiber': 2.7, 'sugar': 5},
            {'id': 9, 'name': 'Milk', 'category': 'Dairy & Eggs', 'calories': 42, 'protein': 3.4, 'fat': 1, 'carbs': 5, 'fiber': 0, 'sugar': 5},
            {'id': 10, 'name': 'Almonds', 'category': 'Nuts', 'calories': 579, 'protein': 21, 'fat': 50, 'carbs': 22, 'fiber': 12, 'sugar': 4}
        ]
        pd.DataFrame(sample_foods).to_csv(food_db_path, index=False)
        print(f"Created sample food database with {len(sample_foods)} items")
    
    print('Starting Food Tracker Platform...')
    print('Access at: http://localhost:5000')
    print('Login at: http://localhost:5000/login')
    print('Debug mode: ON')
    app.run(debug=True, port=5000, use_reloader=True)
import json
import os
from datetime import datetime

class UserManager:
    def __init__(self, json_path='data/users.json'):
        self.json_path = json_path
        self.users = self._load_users()
    
    def _load_users(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # If the file is empty or corrupted, return empty dict
                return {}
        return {}
    
    def _save_users(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def create_user(self, user_id, name, age, weight, height, gender, activity_level, goal):
        bmr = self._calculate_bmr(weight, height, age, gender)
        daily_calories = self._calculate_daily_calories(bmr, activity_level, goal)
        
        user_data = {
            'name': name,
            'age': age,
            'weight': weight,
            'height': height,
            'gender': gender,
            'activity_level': activity_level,
            'goal': goal,
            'bmr': bmr,
            'daily_calories': daily_calories,
            'daily_logs': {},
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        self.users[user_id] = user_data
        self._save_users()
        return user_data
    
    def _calculate_bmr(self, weight, height, age, gender):
        if gender.lower() == 'male':
            return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    def _calculate_daily_calories(self, bmr, activity_level, goal):
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        goal_adjustments = {
            'lose': -500,
            'maintain': 0,
            'gain': 500
        }
        
        maintenance = bmr * activity_multipliers.get(activity_level, 1.2)
        return maintenance + goal_adjustments.get(goal, 0)
    
    def add_food_log(self, user_id, date, food_name, quantity=1, meal_type=None, timestamp=None):
        if user_id not in self.users:
            print(f"DEBUG: User {user_id} not found in users")
            return False
        
        # Initialize daily_logs if it doesn't exist
        if 'daily_logs' not in self.users[user_id]:
            self.users[user_id]['daily_logs'] = {}
        
        if date not in self.users[user_id]['daily_logs']:
            self.users[user_id]['daily_logs'][date] = []
        
        log_entry = {
            'food': food_name,
            'quantity': float(quantity),
            'timestamp': timestamp if timestamp else datetime.now().isoformat()
        }
        
        if meal_type:
            log_entry['meal_type'] = meal_type
        
        self.users[user_id]['daily_logs'][date].append(log_entry)
        self.users[user_id]['updated_at'] = datetime.now().isoformat()
        
        print(f"DEBUG: Added log entry for user {user_id}: {log_entry}")
        self._save_users()
        return True
    
    def get_daily_summary(self, user_id, date):
        if user_id not in self.users:
            return []
        
        if 'daily_logs' not in self.users[user_id]:
            return []
        
        return self.users[user_id]['daily_logs'].get(date, [])
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def update_user(self, user_id, **kwargs):
        """Update user profile information"""
        if user_id not in self.users:
            return None
        
        for key, value in kwargs.items():
            if value is not None:
                self.users[user_id][key] = value
        
        # Recalculate BMR and daily calories if relevant fields changed
        if any(key in kwargs for key in ['weight', 'height', 'age', 'gender', 'activity_level', 'goal']):
            weight = kwargs.get('weight', self.users[user_id]['weight'])
            height = kwargs.get('height', self.users[user_id]['height'])
            age = kwargs.get('age', self.users[user_id]['age'])
            gender = kwargs.get('gender', self.users[user_id]['gender'])
            activity_level = kwargs.get('activity_level', self.users[user_id]['activity_level'])
            goal = kwargs.get('goal', self.users[user_id]['goal'])
            
            bmr = self._calculate_bmr(weight, height, age, gender)
            daily_calories = self._calculate_daily_calories(bmr, activity_level, goal)
            
            self.users[user_id]['bmr'] = bmr
            self.users[user_id]['daily_calories'] = daily_calories
        
        self.users[user_id]['updated_at'] = datetime.now().isoformat()
        self._save_users()
        return self.users[user_id]
    
    def clear_daily_logs(self, user_id, date):
        """Clear all food logs for a specific date"""
        try:
            if user_id in self.users:
                # Initialize daily_logs if not exists
                if 'daily_logs' not in self.users[user_id]:
                    self.users[user_id]['daily_logs'] = {}
                
                # Check if the date exists in daily_logs
                if date in self.users[user_id]['daily_logs']:
                    # Get the count before clearing
                    original_count = len(self.users[user_id]['daily_logs'][date])
                    # Remove the date entry
                    del self.users[user_id]['daily_logs'][date]
                    self.users[user_id]['updated_at'] = datetime.now().isoformat()
                    self._save_users()
                    return True
                else:
                    # No logs for this date
                    return True  # Return True since there's nothing to clear
        except Exception as e:
            print(f"Error clearing logs: {e}")
        
        return False
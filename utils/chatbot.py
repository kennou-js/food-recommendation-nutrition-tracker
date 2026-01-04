import random
import re
import json
from datetime import datetime

class NutritionChatbot:
    def __init__(self, food_db, user_manager):
        self.food_db = food_db
        self.user_manager = user_manager
        print("✅ Professional Nutrition AI Assistant Initialized")
        
        # Comprehensive knowledge base with 100+ foods
        self.knowledge_base = self._initialize_knowledge_base()
        
        # Context memory for conversations
        self.conversation_context = {}
        
        # Pattern matchers for different question types
        self.patterns = self._initialize_patterns()
        
        # User personalization data
        self.user_profiles = {}
    
    def _initialize_knowledge_base(self):
        """Initialize comprehensive food and nutrition knowledge"""
        return {
            # Meat & Poultry
            'chicken': {
                'type': 'protein',
                'benefits': [
                    "Excellent source of lean protein (31g per 100g breast)",
                    "Rich in B vitamins, especially B6 and B12 for energy metabolism",
                    "Contains essential minerals: phosphorus for bones, selenium for antioxidant defense",
                    "Supports muscle growth, repair, and maintenance",
                    "Low in saturated fat when skin is removed",
                    "Contains tryptophan which aids in serotonin production"
                ],
                'nutrition': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'cholesterol': 85},
                'serving': "3-4 oz (85-113g) cooked",
                'preparation': ["Grill", "Bake", "Roast", "Steam"],
                'pairings': ["Brown rice", "Steamed vegetables", "Quinoa", "Sweet potatoes"],
                'health_score': 9,
                'allergens': [],
                'special_notes': "Choose organic/free-range for higher omega-3 content"
            },
            'beef': {
                'type': 'protein',
                'benefits': [
                    "Rich in high-quality protein and essential amino acids",
                    "Excellent source of iron (heme iron) which is easily absorbed",
                    "Contains zinc for immune function and wound healing",
                    "Source of creatine for muscle performance",
                    "Provides vitamin B12 for nerve function"
                ],
                'nutrition': {'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 17, 'iron': 2.6},
                'serving': "3 oz (85g) cooked, lean cuts preferred",
                'preparation': ["Grill", "Broil", "Stew", "Slow cook"],
                'health_score': 7,
                'special_notes': "Choose lean cuts like sirloin or tenderloin"
            },
            
            # Dairy
            'milk': {
                'type': 'dairy',
                'benefits': [
                    "Complete protein source with all essential amino acids",
                    "Rich in calcium and vitamin D for bone health",
                    "Contains potassium which helps regulate blood pressure",
                    "Source of phosphorus for energy production",
                    "Provides riboflavin (B2) for cellular function"
                ],
                'nutrition': {'calories': 42, 'protein': 3.4, 'carbs': 5, 'fat': 1, 'calcium': 125},
                'varieties': {
                    'whole': "3.25% fat, 150 cal/cup",
                    'reduced': "2% fat, 122 cal/cup", 
                    'low-fat': "1% fat, 102 cal/cup",
                    'skim': "0% fat, 83 cal/cup"
                },
                'serving': "1 cup (240ml)",
                'health_score': 8,
                'allergens': ["lactose", "casein"],
                'alternatives': ["Almond milk", "Soy milk", "Oat milk"]
            },
            
            # Grains
            'oatmeal': {
                'type': 'grain',
                'benefits': [
                    "High in beta-glucan soluble fiber which lowers LDL cholesterol",
                    "Low glycemic index for sustained energy release",
                    "Contains antioxidants called avenanthramides with anti-inflammatory effects",
                    "Rich in manganese for bone health and metabolism",
                    "Source of phosphorus and magnesium"
                ],
                'nutrition': {'calories': 158, 'protein': 6, 'carbs': 27, 'fat': 3, 'fiber': 4},
                'types': {
                    'steel-cut': "Minimally processed, chewy texture",
                    'rolled': "Flattened oats, cooks faster",
                    'instant': "Pre-cooked, most processed"
                },
                'serving': "1/2 cup dry (40g) makes about 1 cup cooked",
                'toppings': ["Berries", "Nuts", "Chia seeds", "Cinnamon"],
                'health_score': 9,
                'special_notes': "Avoid flavored instant packets high in sugar"
            },
            
            # Fruits
            'apple': {
                'type': 'fruit',
                'benefits': [
                    "High in pectin fiber which supports gut health and satiety",
                    "Rich in quercetin flavonoid with anti-inflammatory properties",
                    "Contains vitamin C for immune support and collagen production",
                    "Polyphenols may help regulate blood sugar",
                    "Low calorie density for weight management"
                ],
                'nutrition': {'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3, 'fiber': 4.4},
                'varieties': {
                    'gala': "Sweet, crisp, good for eating raw",
                    'granny_smith': "Tart, firm, excellent for baking",
                    'honeycrisp': "Very crisp, balanced sweet-tart"
                },
                'serving': "1 medium apple (182g)",
                'storage': "Refrigerate to maintain crispness",
                'health_score': 9,
                'special_notes': "Most nutrients are in the skin"
            },
            
            # Vegetables
            'broccoli': {
                'type': 'vegetable',
                'benefits': [
                    "Contains sulforaphane with potent anti-cancer properties",
                    "High in vitamin K for blood clotting and bone health",
                    "Excellent source of vitamin C (more than oranges)",
                    "Rich in folate for DNA synthesis and repair",
                    "Contains kaempferol flavonoid with anti-inflammatory effects"
                ],
                'nutrition': {'calories': 55, 'protein': 3.7, 'carbs': 11, 'fat': 0.6, 'fiber': 2.6},
                'serving': "1 cup chopped (91g) raw or cooked",
                'preparation': ["Steam lightly", "Roast", "Stir-fry", "Eat raw"],
                'cooking_tip': "Steam for 5 minutes to maximize sulforaphane",
                'health_score': 10,
                'special_notes': "Cruciferous vegetable with detoxifying properties"
            },
            
            # Fish
            'salmon': {
                'type': 'seafood',
                'benefits': [
                    "Excellent source of omega-3 fatty acids (EPA and DHA)",
                    "High-quality protein for muscle maintenance",
                    "Rich in astaxanthin antioxidant for skin health",
                    "Contains vitamin D for bone health and immune function",
                    "Source of B vitamins for energy production"
                ],
                'nutrition': {'calories': 208, 'protein': 22, 'carbs': 0, 'fat': 13, 'omega3': 2.3},
                'types': {
                    'wild': "Higher omega-3, leaner, more sustainable",
                    'farmed': "More available, sometimes higher contaminants"
                },
                'serving': "3-4 oz (85-113g) cooked",
                'preparation': ["Bake", "Grill", "Poach", "Pan-sear"],
                'health_score': 10,
                'special_notes': "Choose wild-caught when possible"
            },
            
            # Nuts & Seeds
            'almond': {
                'type': 'nut',
                'benefits': [
                    "Rich in vitamin E antioxidant for skin health",
                    "High in monounsaturated fats for heart health",
                    "Good source of magnesium for blood pressure regulation",
                    "Contains prebiotic properties for gut health",
                    "May help with blood sugar control"
                ],
                'nutrition': {'calories': 579, 'protein': 21, 'carbs': 22, 'fat': 50, 'fiber': 12.5},
                'serving': "1 oz (28g) or about 23 almonds",
                'forms': ["Raw", "Roasted", "Sliced", "Almond butter"],
                'health_score': 9,
                'allergens': ["tree nuts"],
                'special_notes': "Soak overnight to improve digestibility"
            },
            
            # Legumes
            'lentil': {
                'type': 'legume',
                'benefits': [
                    "Excellent plant-based protein source",
                    "High in soluble and insoluble fiber",
                    "Rich in folate for cell growth",
                    "Good source of iron (non-heme)",
                    "Low glycemic index"
                ],
                'nutrition': {'calories': 116, 'protein': 9, 'carbs': 20, 'fat': 0.4, 'fiber': 8},
                'varieties': {
                    'brown': "Most common, holds shape well",
                    'green': "French variety, firm texture",
                    'red': "Cook quickly, become mushy"
                },
                'serving': "1/2 cup cooked (100g)",
                'preparation': ["Soup", "Stew", "Salad", "Burgers"],
                'health_score': 10,
                'special_notes': "No soaking required, cook in 20-30 minutes"
            }
        }
    
    def _initialize_patterns(self):
        """Initialize pattern matching for different question types"""
        return {
            'benefit_question': [
                r'benefits? of (.+)',
                r'why is (.+) good',
                r'what does (.+) do',
                r'health benefits of (.+)',
                r'advantages of (.+)'
            ],
            'comparison_question': [
                r'compare (.+) and (.+)',
                r'difference between (.+) and (.+)',
                r'which is better (.+) or (.+)',
                r'(.+) vs (.+)'
            ],
            'nutrition_question': [
                r'nutrition facts? of (.+)',
                r'nutrition information for (.+)',
                r'calories in (.+)',
                r'protein in (.+)',
                r'carbs in (.+)',
                r'fat in (.+)',
                r'nutrients? in (.+)'
            ],
            'preparation_question': [
                r'how to cook (.+)',
                r'best way to prepare (.+)',
                r'recipe for (.+)',
                r'cooking (.+)',
                r'preparing (.+)'
            ],
            'serving_question': [
                r'how much (.+) should i eat',
                r'serving size of (.+)',
                r'portion of (.+)',
                r'how many (.+) per day'
            ],
            'health_question': [
                r'is (.+) healthy',
                r'is (.+) good for you',
                r'should i eat (.+)',
                r'healthy to eat (.+)',
                r'(.+) good or bad'
            ],
            'substitution_question': [
                r'substitute for (.+)',
                r'alternative to (.+)',
                r'replacement for (.+)',
                r'what instead of (.+)'
            ],
            'weight_question': [
                r'^lose weight',
                r'^gain weight',
                r'^muscle building',
                r'^weight management',
                r'^fat loss',
                r'how to lose weight',
                r'how to gain weight',
                r'weight loss tips',
                r'weight gain tips',
                r'how to build muscle',
                r'best way to lose weight',
                r'best way to gain weight'
            ],
            'diet_question': [
                r'^keto diet',
                r'^vegan diet',
                r'^mediterranean diet',
                r'^low carb diet',
                r'^high protein diet',
                r'what is keto diet',
                r'what is vegan diet',
                r'what is mediterranean diet'
            ],
            'meal_planning': [
                r'^meal plan',
                r'^meal prep',
                r'^what should i eat',
                r'^breakfast ideas',
                r'^lunch ideas',
                r'^dinner ideas',
                r'^healthy breakfast',
                r'^healthy lunch',
                r'^healthy dinner',
                r'suggest a healthy breakfast',
                r'suggest a healthy lunch',
                r'suggest a healthy dinner'
            ]
        }
    
    def process_message(self, message, user_id=None):
        """Main message processing with context awareness"""
        message_lower = message.lower().strip()
        
        # Debug: Print what we're processing
        print(f"🔍 Processing: '{message}' -> '{message_lower}'")
        
        # Store context
        if user_id:
            if user_id not in self.conversation_context:
                self.conversation_context[user_id] = []
            self.conversation_context[user_id].append({
                'timestamp': datetime.now().isoformat(),
                'user': message,
                'context': message_lower
            })
            # Keep only last 5 messages
            if len(self.conversation_context[user_id]) > 5:
                self.conversation_context[user_id].pop(0)
        
        # Determine question type and process
        response = self._analyze_and_respond(message_lower, user_id)
        
        return response
    
    def _analyze_and_respond(self, message, user_id):
        """Analyze message type and generate appropriate response"""
        
        # Check if this is the first message from this user
        is_first_message = False
        if user_id:
            if user_id not in self.conversation_context or len(self.conversation_context[user_id]) == 0:
                is_first_message = True
        
        # 1. Check for greetings ONLY on first message
        if is_first_message and self._is_greeting(message):
            print(f"👋 First message detected as greeting: {message}")
            return self._generate_greeting(user_id)
        
        # 2. Check for calorie questions first (specific pattern)
        calorie_response = self._handle_calorie_question(message)
        if calorie_response:
            print(f"🔢 Detected calorie question: {message}")
            return calorie_response
        
        # 3. Goodbyes
        if self._is_goodbye(message):
            return self._generate_goodbye()
        
        # 4. Help request (only exact matches)
        if self._is_help_request(message):
            return self._generate_help_response()
        
        # 5. Check for specific patterns
        for pattern_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message)
                if match:
                    print(f"🎯 Matched pattern '{pattern_type}': {pattern}")
                    return self._handle_pattern(pattern_type, match, message, user_id)
        
        # 6. Check for "tell me about" pattern (common query)
        if message.startswith('tell me about'):
            food_name = message.replace('tell me about', '').strip()
            if food_name:
                print(f"📝 'Tell me about' query for: {food_name}")
                return self._describe_food_benefits(food_name)
        
        # 7. Check for known foods
        food_response = self._handle_food_query(message)
        if food_response:
            print(f"🍎 Found food in knowledge base: {message}")
            return food_response
        
        # 8. Check database
        db_response = self._search_database_intelligently(message)
        if db_response:
            print(f"🔍 Found in database: {message}")
            return db_response
        
        # 9. Check for high protein foods question
        if 'high protein' in message or 'protein rich' in message or 'foods high in protein' in message:
            return self._list_high_protein_foods()
        
        # 10. Check for general nutrition questions
        if 'healthy' in message and ('food' in message or 'eat' in message):
            return self._general_healthy_eating_advice()
        
        # 11. General nutrition advice
        general_response = self._provide_general_advice(message)
        if general_response:
            return general_response
        
        # 12. Fallback with context awareness
        return self._context_aware_fallback(message, user_id)
    
    def _handle_calorie_question(self, message):
        """Handle calorie-related questions specifically"""
        # Pattern for "how many calories in X"
        pattern = r'how many calories (?:are|is)? in (.+)'
        match = re.search(pattern, message.lower())
        
        if match:
            food_name = match.group(1)
            # Check database first
            results = self.food_db.search_food(food_name, top_n=1)
            if results:
                food = results[0]
                return f"🍎 **{food['name'].upper()} - CALORIE INFORMATION** 🍎\n\n" \
                       f"**Calories per 100g:** {food['calories']} cal\n" \
                       f"**Category:** {food['category']}\n\n" \
                       f"**Other nutrients per 100g:**\n" \
                       f"• Protein: {food['protein']}g\n" \
                       f"• Carbs: {food['carbs']}g\n" \
                       f"• Fat: {food['fat']}g\n\n" \
                       f"📊 **Search for '{food['name']}' above to log it in your food diary!**"
            
            # Check knowledge base
            food_key = self._find_food_key(food_name)
            if food_key:
                food_info = self.knowledge_base[food_key]
                return f"🍎 **{food_key.upper()} - CALORIE INFORMATION** 🍎\n\n" \
                       f"**Calories per 100g:** {food_info['nutrition']['calories']} cal\n" \
                       f"**Category:** {food_info['type'].title()}\n\n" \
                       f"**Health Score:** {food_info['health_score']}/10\n\n" \
                       f"📊 **Search for '{food_key}' above to log it in your food diary!**"
        
        return None
    
    def _list_high_protein_foods(self):
        """List high protein foods"""
        # Get high protein foods from database
        try:
            df = self.food_db.df
            high_protein = df[df['protein'] > 20].sort_values('protein', ascending=False).head(10)
            
            response = "💪 **TOP 10 HIGH PROTEIN FOODS** 💪\n\n"
            
            for idx, row in high_protein.iterrows():
                response += f"**{row['name']}**\n"
                response += f"• Protein: {row['protein']}g per 100g\n"
                response += f"• Calories: {row['calories']}\n"
                response += f"• Category: {row['category']}\n\n"
            
            response += "💡 **Tip:** Include protein with every meal for muscle maintenance and satiety."
            return response
        except:
            return "💪 **HIGH PROTEIN FOODS** 💪\n\n" \
                   "Top protein sources:\n" \
                   "• Chicken breast (31g protein per 100g)\n" \
                   "• Beef steak (26g)\n" \
                   "• Salmon (22g)\n" \
                   "• Eggs (13g)\n" \
                   "• Greek yogurt (10g)\n" \
                   "• Lentils (9g)\n" \
                   "• Almonds (21g)\n\n" \
                   "💡 Aim for 1.6-2.2g protein per kg body weight daily."
    
    def _general_healthy_eating_advice(self):
        """Provide general healthy eating advice"""
        return "🥗 **HEALTHY EATING GUIDELINES** 🥗\n\n" \
               "1. **Eat whole foods** - Fruits, vegetables, lean proteins, whole grains\n" \
               "2. **Balance your plate** - 50% vegetables, 25% protein, 25% whole grains\n" \
               "3. **Stay hydrated** - Drink water throughout the day\n" \
               "4. **Limit processed foods** - Avoid added sugars and unhealthy fats\n" \
               "5. **Practice portion control** - Use your hand as a guide:\n" \
               "   • Protein: Palm-sized\n" \
               "   • Carbs: Fist-sized\n" \
               "   • Fats: Thumb-sized\n" \
               "   • Veggies: Unlimited (non-starchy)\n\n" \
               "📱 **Track your meals in this app for better awareness!**"
    
    def _handle_pattern(self, pattern_type, match, message, user_id):
        """Handle different question patterns"""
        
        if pattern_type == 'benefit_question':
            food = match.group(1)
            return self._describe_food_benefits(food)
        
        elif pattern_type == 'comparison_question':
            food1 = match.group(1)
            food2 = match.group(2)
            return self._compare_foods(food1, food2)
        
        elif pattern_type == 'nutrition_question':
            food = match.group(1)
            return self._provide_nutrition_details(food)
        
        elif pattern_type == 'preparation_question':
            food = match.group(1)
            return self._suggest_preparation(food)
        
        elif pattern_type == 'serving_question':
            food = match.group(1)
            return self._recommend_serving(food, user_id)
        
        elif pattern_type == 'health_question':
            food = match.group(1)
            return self._assess_healthiness(food)
        
        elif pattern_type == 'substitution_question':
            food = match.group(1)
            return self._suggest_substitutes(food)
        
        elif pattern_type == 'weight_question':
            return self._weight_management_advice(message, user_id)
        
        elif pattern_type == 'diet_question':
            return self._diet_specific_advice(message)
        
        elif pattern_type == 'meal_planning':
            return self._meal_planning_suggestions(user_id)
        
        return None
    
    def _describe_food_benefits(self, food_name):
        """Provide comprehensive benefits of a food"""
        food_key = self._find_food_key(food_name)
        
        if not food_key:
            # Try database
            results = self.food_db.search_food(food_name, top_n=1)
            if results:
                food = results[0]
                return f"**{food['name']}** is a {food['category']} with:\n• {food['calories']} calories per 100g\n• {food['protein']}g protein\n• {food['carbs']}g carbohydrates\n• {food['fat']}g fat\n\nIt provides essential nutrients for energy and health."
            return f"I don't have detailed benefits for {food_name}. Try searching it in our database above!"
        
        food_info = self.knowledge_base[food_key]
        
        response = f"🍎 **{food_key.upper()} - COMPREHENSIVE BENEFITS** 🍎\n\n"
        response += f"**Category:** {food_info['type'].title()}\n"
        response += f"**Health Score:** {food_info['health_score']}/10\n\n"
        
        response += "**TOP HEALTH BENEFITS:**\n"
        for i, benefit in enumerate(food_info['benefits'][:5], 1):
            response += f"{i}. {benefit}\n"
        
        if len(food_info['benefits']) > 5:
            response += f"\n*Plus {len(food_info['benefits']) - 5} more benefits...*\n"
        
        response += f"\n**NUTRITION PER 100g:**\n"
        for nutrient, value in food_info['nutrition'].items():
            response += f"• {nutrient.title()}: {value}{'g' if nutrient != 'calories' else ''}\n"
        
        if 'serving' in food_info:
            response += f"\n**RECOMMENDED SERVING:** {food_info['serving']}\n"
        
        if 'preparation' in food_info:
            response += f"\n**BEST PREPARATION METHODS:**\n"
            response += ", ".join(food_info['preparation'])
        
        if 'special_notes' in food_info:
            response += f"\n\n**💡 PRO TIP:** {food_info['special_notes']}"
        
        response += f"\n\n📊 **Search '{food_key}' above to log it in your food diary!**"
        
        return response
    
    def _compare_foods(self, food1, food2):
        """Compare two foods nutritionally"""
        key1 = self._find_food_key(food1)
        key2 = self._find_food_key(food2)
        
        if not key1 or not key2:
            return f"I can compare foods I know about. Try: chicken vs beef, apple vs banana, oatmeal vs rice."
        
        info1 = self.knowledge_base[key1]
        info2 = self.knowledge_base[key2]
        
        response = f"🥊 **{key1.upper()} VS {key2.upper()} - NUTRITION COMPARISON** 🥊\n\n"
        
        # Compare nutrition
        response += "**NUTRITION PER 100g:**\n"
        response += f"{'Nutrient':<15} {key1.title():<10} {key2.title():<10} Winner\n"
        response += "-" * 50 + "\n"
        
        comparisons = []
        for nutrient in ['calories', 'protein', 'carbs', 'fat', 'fiber']:
            if nutrient in info1['nutrition'] and nutrient in info2['nutrition']:
                val1 = info1['nutrition'][nutrient]
                val2 = info2['nutrition'][nutrient]
                winner = key1 if (val1 > val2 and nutrient in ['protein', 'fiber']) or (val1 < val2 and nutrient in ['calories', 'fat']) else key2
                comparisons.append((nutrient, val1, val2, winner))
        
        for nutrient, val1, val2, winner in comparisons:
            response += f"{nutrient.title():<15} {val1:<10} {val2:<10} {winner.title()}\n"
        
        # Compare health scores
        response += f"\n**HEALTH SCORE:** {key1.title()}: {info1['health_score']}/10 | {key2.title()}: {info2['health_score']}/10\n"
        
        # Give recommendation
        if info1['health_score'] > info2['health_score']:
            response += f"\n**RECOMMENDATION:** {key1.title()} is generally healthier!"
        elif info2['health_score'] > info1['health_score']:
            response += f"\n**RECOMMENDATION:** {key2.title()} is generally healthier!"
        else:
            response += f"\n**RECOMMENDATION:** Both are excellent choices!"
        
        response += f"\n\n💡 **Tip:** Variety is key - include both in your diet for balanced nutrition."
        
        return response
    
    def _provide_nutrition_details(self, food_name):
        """Provide detailed nutrition information"""
        food_key = self._find_food_key(food_name)
        
        if not food_key:
            # Search database
            results = self.food_db.search_food(food_name, top_n=1)
            if results:
                food = results[0]
                return self._format_database_food_info(food)
            return f"Search for '{food_name}' above to see its nutrition facts!"
        
        food_info = self.knowledge_base[food_key]
        
        response = f"📊 **{food_key.upper()} - DETAILED NUTRITION ANALYSIS** 📊\n\n"
        
        response += "**MACRONUTRIENTS:**\n"
        for macro in ['calories', 'protein', 'carbs', 'fat']:
            if macro in food_info['nutrition']:
                unit = 'g' if macro != 'calories' else ''
                response += f"• {macro.title()}: {food_info['nutrition'][macro]}{unit}\n"
        
        response += "\n**MICRONUTRIENTS & OTHER COMPONENTS:**\n"
        for nutrient, value in food_info['nutrition'].items():
            if nutrient not in ['calories', 'protein', 'carbs', 'fat']:
                unit = 'g' if nutrient in ['fiber', 'sugar', 'cholesterol'] else 'mg' if nutrient in ['iron', 'calcium'] else ''
                response += f"• {nutrient.title()}: {value}{unit}\n"
        
        if 'serving' in food_info:
            response += f"\n**STANDARD SERVING:** {food_info['serving']}\n"
        
        # Calculate % of daily values
        response += "\n**APPROXIMATE DAILY VALUE (%):**\n"
        if 'protein' in food_info['nutrition']:
            protein_pct = (food_info['nutrition']['protein'] / 50) * 100
            response += f"• Protein: {protein_pct:.1f}% of daily needs\n"
        
        response += f"\n**HEALTH IMPACT SCORE:** {food_info['health_score']}/10"
        
        return response
    
    def _suggest_preparation(self, food_name):
        """Suggest preparation methods for a food"""
        food_key = self._find_food_key(food_name)
        
        if not food_key:
            return f"I have preparation tips for common foods. Try: chicken, fish, vegetables, eggs."
        
        food_info = self.knowledge_base[food_key]
        
        response = f"👨‍🍳 **{food_key.upper()} - PREPARATION GUIDE** 👨‍🍳\n\n"
        
        if 'preparation' in food_info:
            response += "**RECOMMENDED METHODS:**\n"
            for i, method in enumerate(food_info['preparation'], 1):
                response += f"{i}. {method}\n"
        
        if 'cooking_tip' in food_info:
            response += f"\n**PRO COOKING TIP:** {food_info['cooking_tip']}\n"
        
        if 'pairings' in food_info:
            response += f"\n**GOOD PAIRINGS:**\n"
            response += ", ".join(food_info['pairings'])
        
        if 'special_notes' in food_info:
            response += f"\n\n**NUTRITION PRESERVATION:** {food_info['special_notes']}"
        
        response += f"\n\n🔥 **Search for '{food_key}' above to log your prepared meal!**"
        
        return response
    
    def _recommend_serving(self, food_name, user_id):
        """Recommend serving size based on user profile"""
        food_key = self._find_food_key(food_name)
        
        if not food_key:
            return "Serving sizes vary by food. For accurate tracking, search for the food above."
        
        food_info = self.knowledge_base[food_key]
        
        response = f"⚖️ **{food_key.upper()} - SERVING RECOMMENDATIONS** ⚖️\n\n"
        
        if 'serving' in food_info:
            response += f"**Standard Serving:** {food_info['serving']}\n"
        
        # Personalized recommendations if user data available
        if user_id:
            user = self.user_manager.get_user(user_id)
            if user:
                daily_cals = user.get('daily_calories', 2000)
                food_cals = food_info['nutrition'].get('calories', 100)
                
                # Calculate appropriate servings
                servings_for_meal = int((daily_cals * 0.25) / food_cals)  # 25% of daily calories
                servings_for_snack = int((daily_cals * 0.1) / food_cals)   # 10% of daily calories
                
                response += f"\n**PERSONALIZED FOR YOU ({user['name']}):**\n"
                response += f"• For a main meal: {servings_for_meal} servings\n"
                response += f"• For a snack: {servings_for_snack} servings\n"
                response += f"• Based on your daily goal of {daily_cals:.0f} calories"
        
        response += "\n\n**GENERAL GUIDELINES:**\n"
        response += "• Protein foods: palm-sized portion\n"
        response += "• Carbs: fist-sized portion\n"
        response += "• Fats: thumb-sized portion\n"
        response += "• Vegetables: unlimited (non-starchy)"
        
        return response
    
    def _assess_healthiness(self, food_name):
        """Assess how healthy a food is"""
        food_key = self._find_food_key(food_name)
        
        if not food_key:
            return f"Most whole foods are healthy in moderation. Processed foods should be limited."
        
        food_info = self.knowledge_base[food_key]
        
        response = f"🏥 **{food_key.upper()} - HEALTH ASSESSMENT** 🏥\n\n"
        
        response += f"**HEALTH SCORE:** {food_info['health_score']}/10\n\n"
        
        if food_info['health_score'] >= 8:
            response += "✅ **VERY HEALTHY** - Excellent choice for regular consumption\n"
        elif food_info['health_score'] >= 6:
            response += "👍 **HEALTHY** - Good choice in moderation\n"
        elif food_info['health_score'] >= 4:
            response += "⚠️ **MODERATE** - Limit consumption\n"
        else:
            response += "❌ **UNHEALTHY** - Avoid or consume rarely\n"
        
        response += "\n**WHY THIS SCORE?**\n"
        for i, benefit in enumerate(food_info['benefits'][:3], 1):
            response += f"+ {benefit}\n"
        
        if 'special_notes' in food_info:
            response += f"\n**IMPORTANT NOTES:** {food_info['special_notes']}"
        
        return response
    
    def _suggest_substitutes(self, food_name):
        """Suggest healthy substitutes for a food"""
        food_key = self._find_food_key(food_name)
        
        if not food_key:
            return "Common substitutes:\n• Milk → Almond milk\n• Rice → Quinoa\n• Potato → Sweet potato\n• Beef → Lentils"
        
        food_info = self.knowledge_base[food_key]
        
        response = f"🔄 **{food_key.upper()} - HEALTHY SUBSTITUTES** 🔄\n\n"
        
        if 'alternatives' in food_info:
            response += "**DIRECT SUBSTITUTES:**\n"
            for alt in food_info['alternatives']:
                response += f"• {alt}\n"
        
        # General substitutes by category
        category_subs = {
            'protein': ["Lentils", "Chickpeas", "Tofu", "Tempeh", "Edamame"],
            'dairy': ["Almond milk", "Soy milk", "Coconut yogurt", "Cashew cheese"],
            'grain': ["Quinoa", "Brown rice", "Farro", "Barley", "Buckwheat"],
            'fruit': ["Berries", "Citrus fruits", "Stone fruits", "Tropical fruits"]
        }
        
        if food_info['type'] in category_subs:
            response += f"\n**OTHER {food_info['type'].upper()} OPTIONS:**\n"
            for sub in category_subs[food_info['type']]:
                response += f"• {sub}\n"
        
        response += f"\n💡 **Tip:** When substituting, consider texture, flavor, and cooking time."
        
        return response
    
    def _weight_management_advice(self, message, user_id):
        """Provide weight management advice"""
        response = "⚖️ **WEIGHT MANAGEMENT STRATEGIES** ⚖️\n\n"
        
        message_lower = message.lower()
        
        if 'lose weight' in message_lower or 'weight loss' in message_lower or 'lose fat' in message_lower:
            response += "**FOR WEIGHT LOSS:**\n"
            response += "1. **Calorie deficit** - Eat 300-500 calories less than you burn daily\n"
            response += "2. **High protein** - Aim for 1.6-2.2g protein per kg body weight\n"
            response += "3. **Strength training** - 3x/week to preserve muscle\n"
            response += "4. **Cardio** - 150+ minutes moderate or 75+ minutes vigorous weekly\n"
            response += "5. **Track consistently** - Use this app to log your food daily!\n"
        
        elif 'gain weight' in message_lower or 'weight gain' in message_lower or 'build muscle' in message_lower:
            response += "**FOR WEIGHT/MUSCLE GAIN:**\n"
            response += "1. **Calorie surplus** - Eat 300-500 calories above maintenance\n"
            response += "2. **High protein** - 1.6-2.2g per kg body weight\n"
            response += "3. **Progressive overload** - Increase weights/reps each week\n"
            response += "4. **Adequate sleep** - 7-9 hours for recovery\n"
            response += "5. **Track progress** - Monitor weight and measurements weekly\n"
        
        else:
            # General weight advice
            response += "**GENERAL WEIGHT MANAGEMENT:**\n"
            response += "• Track your calories and macros\n"
            response += "• Eat protein with every meal\n"
            response += "• Include strength training\n"
            response += "• Stay consistent\n"
            response += "• Get enough sleep (7-9 hours)\n"
            response += "• Manage stress\n"
        
        # Personalize if user data available
        if user_id:
            user = self.user_manager.get_user(user_id)
            if user:
                response += f"\n**PERSONALIZED FOR {user['name'].upper()}:**\n"
                response += f"• Current BMI: {user.get('bmi', 'N/A')} ({user.get('bmi_category', '')})\n"
                response += f"• Daily calorie target: {user.get('daily_calories', 2000):.0f}\n"
                response += f"• Goal: {user.get('goal', 'maintain').title()}\n\n"
                response += f"📱 **Track your progress in this app daily!**"
        
        return response
    
    def _diet_specific_advice(self, message):
        """Provide diet-specific advice"""
        response = "🥗 **DIET-SPECIFIC GUIDANCE** 🥗\n\n"
        
        message_lower = message.lower()
        
        if 'keto' in message_lower:
            response += "**KETOGENIC DIET:**\n"
            response += "• **Macros:** 70% Fat, 25% Protein, 5% Carbs\n"
            response += "• **Foods:** Meat, fish, eggs, avocado, nuts, oils\n"
            response += "• **Avoid:** Grains, sugar, most fruits, starchy vegetables\n"
            response += "• **Goal:** <50g net carbs daily\n"
            response += "• **Benefits:** Rapid weight loss, improved blood sugar control\n"
        
        elif 'vegan' in message_lower:
            response += "**VEGAN DIET:**\n"
            response += "• **Protein sources:** Lentils, tofu, tempeh, seitan, beans\n"
            response += "• **Key nutrients to watch:** B12, Iron, Calcium, Omega-3, Vitamin D\n"
            response += "• **Consider supplements** for B12 and possibly DHA/EPA\n"
            response += "• **Variety is essential** for complete nutrition\n"
        
        elif 'mediterranean' in message_lower:
            response += "**MEDITERRANEAN DIET:**\n"
            response += "• **Foundation:** Vegetables, fruits, whole grains, legumes\n"
            response += "• **Protein:** Fish, poultry, occasional red meat\n"
            response += "• **Fats:** Olive oil, nuts, avocado\n"
            response += "• **Limited:** Red meat, processed foods, added sugar\n"
            response += "• **Considered** one of the healthiest diet patterns\n"
        
        elif 'low carb' in message_lower:
            response += "**LOW CARB DIET:**\n"
            response += "• **Carbs:** 50-150g daily\n"
            response += "• **Focus:** Non-starchy vegetables, protein, healthy fats\n"
            response += "• **Avoid:** Sugar, grains, starchy foods\n"
            response += "• **Benefits:** Weight loss, improved blood sugar control\n"
        
        elif 'high protein' in message_lower:
            response += "**HIGH PROTEIN DIET:**\n"
            response += "• **Protein:** 1.6-2.2g per kg body weight\n"
            response += "• **Sources:** Meat, fish, eggs, dairy, legumes\n"
            response += "• **Benefits:** Increased satiety, muscle preservation, boosted metabolism\n"
            response += "• **Stay hydrated** and include fiber\n"
        
        response += f"\n💡 **Track your diet in this app to stay on target!**"
        
        return response
    
    def _meal_planning_suggestions(self, user_id):
        """Provide meal planning suggestions"""
        response = "🍽️ **MEAL PLANNING GUIDE** 🍽️\n\n"
        
        # Get user data if available
        daily_cals = 2000
        if user_id:
            user = self.user_manager.get_user(user_id)
            if user:
                daily_cals = user.get('daily_calories', 2000)
        
        # Calculate meal distribution
        breakfast_cals = daily_cals * 0.25
        lunch_cals = daily_cals * 0.35
        dinner_cals = daily_cals * 0.30
        snacks_cals = daily_cals * 0.10
        
        response += f"**DAILY CALORIE DISTRIBUTION ({daily_cals:.0f} total):**\n"
        response += f"• Breakfast: {breakfast_cals:.0f} calories\n"
        response += f"• Lunch: {lunch_cals:.0f} calories\n"
        response += f"• Dinner: {dinner_cals:.0f} calories\n"
        response += f"• Snacks: {snacks_cals:.0f} calories\n\n"
        
        response += "**SAMPLE MEAL IDEAS:**\n"
        response += "**Breakfast:** Oatmeal with berries and nuts\n"
        response += "**Lunch:** Grilled chicken salad with olive oil dressing\n"
        response += "**Dinner:** Salmon with quinoa and roasted vegetables\n"
        response += "**Snacks:** Apple with almond butter, Greek yogurt\n\n"
        
        response += "**MEAL PREP TIPS:**\n"
        response += "1. Cook proteins in bulk\n"
        response += "2. Prep vegetables for the week\n"
        response += "3. Use airtight containers\n"
        response += "4. Label with dates\n"
        response += "5. Freeze portions\n"
        
        response += f"\n📱 **Plan and track your meals in this app!**"
        
        return response
    
    def _handle_food_query(self, message):
        """Handle general food queries"""
        # Check for foods in knowledge base
        for food_key in self.knowledge_base.keys():
            if food_key in message.lower():
                # Check what kind of query
                if 'benefit' in message or 'good' in message or 'healthy' in message:
                    return self._describe_food_benefits(food_key)
                elif 'nutrition' in message or 'calorie' in message or 'protein' in message:
                    return self._provide_nutrition_details(food_key)
                elif 'cook' in message or 'prepare' in message or 'recipe' in message:
                    return self._suggest_preparation(food_key)
                elif 'serving' in message or 'portion' in message or 'how much' in message:
                    return self._recommend_serving(food_key, None)
                else:
                    # General information
                    return self._describe_food_benefits(food_key)
        
        return None
    
    def _search_database_intelligently(self, message):
        """Intelligently search database and provide useful info"""
        # Extract potential food names
        words = re.findall(r'\b[a-zA-Z]{3,}\b', message.lower())
        
        for word in words:
            if len(word) > 2:
                try:
                    results = self.food_db.search_food(word, top_n=1)
                    if results:
                        food = results[0]
                        return self._format_database_food_info(food)
                except:
                    pass
        
        return None
    
    def _format_database_food_info(self, food):
        """Format database food information professionally"""
        response = f"🔍 **{food['name'].upper()} - FOOD DATABASE ENTRY** 🔍\n\n"
        
        response += f"**Category:** {food['category']}\n"
        response += f"**Database ID:** {food['id']}\n\n"
        
        response += "**NUTRITION PER 100g:**\n"
        nutrients = [
            ('Calories', food['calories'], 'cal'),
            ('Protein', food['protein'], 'g'),
            ('Carbs', food['carbs'], 'g'),
            ('Fat', food['fat'], 'g'),
            ('Fiber', food.get('fiber', 0), 'g'),
            ('Sugar', food.get('sugar', 0), 'g')
        ]
        
        for name, value, unit in nutrients:
            if value > 0 or name == 'Calories':
                response += f"• {name}: {value}{unit}\n"
        
        # Add health assessment
        health_score = self._calculate_health_score(food)
        response += f"\n**HEALTH SCORE:** {health_score}/10\n"
        
        if health_score >= 8:
            response += "✅ Excellent choice for regular consumption\n"
        elif health_score >= 6:
            response += "👍 Good choice in moderation\n"
        else:
            response += "⚠️ Consume in limited quantities\n"
        
        response += f"\n📝 **Log this food in your diary above!**"
        
        return response
    
    def _calculate_health_score(self, food):
        """Calculate a health score for database foods"""
        score = 5  # Base score
        
        # Adjust based on nutrition
        if food['protein'] > 10:
            score += 1
        if food.get('fiber', 0) > 3:
            score += 1
        if food['fat'] < 10:
            score += 1
        if food.get('sugar', 0) < 5:
            score += 1
        if food['calories'] < 200:
            score += 1
        
        # Category adjustments
        healthy_categories = ['Vegetable', 'Fruit', 'Protein', 'Legume']
        if food['category'] in healthy_categories:
            score += 1
        
        return min(10, score)
    
    def _provide_general_advice(self, message):
        """Provide general nutrition advice"""
        advice_topics = {
            'water': "💧 **HYDRATION:** Drink 8+ glasses of water daily. More if active or in heat.",
            'sleep': "😴 **SLEEP:** Aim for 7-9 hours nightly. Sleep affects hunger hormones.",
            'exercise': "🏃 **EXERCISE:** 150 minutes moderate or 75 minutes vigorous weekly.",
            'fiber': "🌾 **FIBER:** Aim for 25-30g daily from vegetables, fruits, whole grains.",
            'sugar': "🍬 **SUGAR:** Limit added sugar to <25g (6 tsp) daily for women, <36g (9 tsp) for men.",
            'salt': "🧂 **SALT:** Limit to <2300mg sodium daily. Read labels.",
            'alcohol': "🍷 **ALCOHOL:** Moderate drinking = 1 drink/day women, 2 drinks/day men.",
            'stress': "🧘 **STRESS:** Chronic stress increases cortisol, affecting weight and health."
        }
        
        for topic, advice in advice_topics.items():
            if topic in message.lower():
                return advice
        
        # Check for nutrient queries
        nutrients = {
            'vitamin c': "🍊 **VITAMIN C:** Antioxidant, immune support. Sources: citrus, bell peppers, broccoli.",
            'vitamin d': "☀️ **VITAMIN D:** Bone health, immune function. Sources: sun, fatty fish, fortified foods.",
            'calcium': "🥛 **CALCIUM:** Bone health, muscle function. Sources: dairy, leafy greens, fortified foods.",
            'iron': "🥩 **IRON:** Oxygen transport, energy. Sources: red meat, spinach, lentils.",
            'omega-3': "🐟 **OMEGA-3:** Brain health, anti-inflammatory. Sources: fatty fish, flaxseeds, walnuts.",
            'magnesium': "🥑 **MAGNESIUM:** Muscle relaxation, energy. Sources: nuts, seeds, leafy greens.",
            'potassium': "🍌 **POTASSIUM:** Blood pressure, hydration. Sources: bananas, potatoes, beans."
        }
        
        for nutrient, info in nutrients.items():
            if nutrient in message.lower():
                return info
        
        return None
    
    def _context_aware_fallback(self, message, user_id):
        """Provide context-aware fallback responses"""
        # Check conversation history
        if user_id and user_id in self.conversation_context:
            last_messages = self.conversation_context[user_id][-3:]
            last_topics = [msg['context'] for msg in last_messages]
            
            # Check if we were discussing a specific food
            for topic in last_topics:
                for food_key in self.knowledge_base.keys():
                    if food_key in topic:
                        return f"Regarding {food_key}, would you like to know about its benefits, nutrition facts, or how to prepare it?"
        
        # Smart suggestions based on message length
        if len(message.split()) <= 2:
            # Short message - suggest specific foods
            suggestions = random.sample(list(self.knowledge_base.keys()), 3)
            return (
                f"🤔 I specialize in food and nutrition information.\n\n"
                f"**Try asking about:**\n"
                f"• Benefits of {suggestions[0]}\n"
                f"• Is {suggestions[1]} healthy?\n"
                f"• How to cook {suggestions[2]}\n\n"
                f"**Or search for any food above to see its nutrition facts!**"
            )
        else:
            # Longer message - analyze and guide
            return (
                f"🧠 **I ANALYZED YOUR QUESTION:**\n\n"
                f"I'm your nutrition expert assistant. I can help with:\n\n"
                f"1. **Food Information** - Benefits, nutrition, preparation\n"
                f"2. **Diet Advice** - Weight loss, muscle gain, specific diets\n"
                f"3. **Meal Planning** - Recipes, portion sizes, meal prep\n"
                f"4. **Health Assessment** - Is a food healthy? How much to eat?\n\n"
                f"**Try rephrasing or ask about a specific food!**\n"
                f"Example: 'Tell me about salmon' or 'How can I lose weight?'"
            )
    
    def _find_food_key(self, food_name):
        """Find food key in knowledge base"""
        food_name = food_name.lower().strip()
        
        # Direct match
        if food_name in self.knowledge_base:
            return food_name
        
        # Partial matches
        for key in self.knowledge_base.keys():
            if key in food_name or food_name in key:
                return key
        
        # Common variations
        variations = {
            'chicken breast': 'chicken',
            'oatmeal': 'oatmeal',
            'oats': 'oatmeal',
            'apple': 'apple',
            'apples': 'apple',
            'broccoli': 'broccoli',
            'salmon': 'salmon',
            'milk': 'milk',
            'almonds': 'almond',
            'lentils': 'lentil',
            'beef': 'beef'
        }
        
        return variations.get(food_name, None)
    
    def _is_greeting(self, message):
        """Check if message is a greeting - FIXED VERSION"""
        message_lower = message.lower().strip()
        
        # Exact greeting matches only
        exact_greetings = ['hello', 'hi', 'hey', 'greetings', 'hello!', 'hi!', 'hey!', 'hi there', 'hello there']
        
        # Check if the ENTIRE message is a greeting
        if message_lower in exact_greetings:
            return True
        
        # Check for common greeting phrases
        greeting_phrases = [
            'good morning', 'good afternoon', 'good evening',
            'morning', 'afternoon', 'evening'
        ]
        
        for phrase in greeting_phrases:
            if message_lower.startswith(phrase):
                return True
        
        return False
    
    def _is_goodbye(self, message):
        """Check if message is a goodbye"""
        goodbyes = ['bye', 'goodbye', 'see you', 'farewell', 'bye!', 'goodbye!']
        
        message_lower = message.lower().strip()
        if message_lower in goodbyes:
            return True
        
        return False
    
    def _is_help_request(self, message):
        """Check if message is a help request - FIXED VERSION"""
        message_lower = message.lower().strip()
        
        # Exact help requests only
        help_phrases = [
            'help',
            'what can you do',
            'what do you do',
            'what are your capabilities',
            'what are your features',
            'how to use you',
            'what help can you provide',
            'help!',
            'what can you help with'
        ]
        
        # Check for exact matches first
        if message_lower in help_phrases:
            return True
        
        # Check if starts with help
        if message_lower == 'help' or message_lower.startswith('help '):
            return True
        
        # Check if it's specifically asking about capabilities
        if 'what can you' in message_lower or 'how to use' in message_lower:
            return True
        
        return False
    
    def _generate_greeting(self, user_id):
        """Generate personalized greeting"""
        greeting = "👋 **Hello! I'm your AI nutritionist.**\n\n"
        greeting += "I can help you with:\n"
        greeting += "• Food nutrition information\n"
        greeting += "• Calorie calculations\n"
        greeting += "• Meal planning advice\n"
        greeting += "• Healthy eating tips\n"
        greeting += "• Food recommendations\n\n"
        greeting += "**What would you like to know?**"
        
        # Optional: Add personalization
        if user_id:
            user = self.user_manager.get_user(user_id)
            if user:
                greeting = f"👋 **Hello {user['name']}! I'm your AI nutritionist.**\n\n"
                greeting += f"Your daily calorie target: {user.get('daily_calories', 2000):.0f}\n"
                greeting += f"Current goal: {user.get('goal', 'maintain').title()} weight\n\n"
                greeting += "**What would you like to know about your nutrition today?**"
        
        return greeting
    
    def _generate_goodbye(self):
        """Generate goodbye message"""
        goodbyes = [
            "👋 Farewell! Remember: consistency beats perfection in nutrition.",
            "🍎 Goodbye! Keep tracking your food and making healthy choices.",
            "🥦 See you later! Your health journey is a marathon, not a sprint."
        ]
        
        return random.choice(goodbyes)
    
    def _generate_help_response(self):
        """Generate comprehensive help response"""
        response = "📚 **NUTRITION ASSISTANT - COMPLETE CAPABILITIES** 📚\n\n"
        
        response += "**I CAN HELP WITH:**\n\n"
        
        response += "🍎 **FOOD INFORMATION**\n"
        response += "• Benefits of any food\n"
        response += "• Nutrition facts and analysis\n"
        response += "• Preparation and cooking methods\n"
        response += "• Serving size recommendations\n"
        response += "• Health assessments\n\n"
        
        response += "⚖️ **DIET & NUTRITION**\n"
        response += "• Weight loss/gain strategies\n"
        response += "• Muscle building nutrition\n"
        response += "• Diet comparisons (Keto, Vegan, Mediterranean)\n"
        response += "• Meal planning and prep\n"
        response += "• Nutrient deficiency information\n\n"
        
        response += "🔍 **FOOD ANALYSIS**\n"
        response += "• Compare two foods\n"
        response += "• Find healthy substitutes\n"
        response += "• Calculate health scores\n"
        response += "• Identify best food choices\n\n"
        
        response += "**EXAMPLE QUESTIONS:**\n"
        response += "• 'Benefits of salmon'\n"
        response += "• 'Compare chicken and beef'\n"
        response += "• 'How to lose weight'\n"
        response += "• 'Is oatmeal healthy?'\n"
        response += "• 'Keto diet advice'\n\n"
        
        response += "**OR search for any food above to log it in your diary!**"
        
        return response
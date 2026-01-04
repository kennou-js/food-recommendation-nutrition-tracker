class NutritionCalculator:
    @staticmethod
    def calculate_bmi(weight_kg, height_cm):
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    @staticmethod
    def bmi_category(bmi):
        if bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= bmi < 25:
            return 'Normal weight'
        elif 25 <= bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
    
    @staticmethod
    def calculate_tdee(bmr, activity_level):
        multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        return bmr * multipliers.get(activity_level, 1.2)
    
    @staticmethod
    def calculate_macros(calories, protein_ratio=0.3, fat_ratio=0.3, carb_ratio=0.4):
        protein_cals = calories * protein_ratio
        fat_cals = calories * fat_ratio
        carb_cals = calories * carb_ratio
        
        return {
            'protein_grams': protein_cals / 4,
            'fat_grams': fat_cals / 9,
            'carb_grams': carb_cals / 4,
            'protein_percent': protein_ratio * 100,
            'fat_percent': fat_ratio * 100,
            'carb_percent': carb_ratio * 100
        }
    
    @staticmethod
    def water_intake_recommendation(weight_kg, activity_level='moderate'):
        base_water = weight_kg * 0.033
        
        if activity_level == 'light':
            return base_water + 0.3
        elif activity_level == 'moderate':
            return base_water + 0.5
        elif activity_level == 'active':
            return base_water + 0.8
        elif activity_level == 'very_active':
            return base_water + 1.0
        
        return base_water
    
    @staticmethod
    def calculate_deficit_surplus(current_calories, target_calories):
        difference = current_calories - target_calories
        if difference > 0:
            return f'Surplus: +{difference:.0f} calories'
        elif difference < 0:
            return f'Deficit: {difference:.0f} calories'
        else:
            return 'On target'

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import os

class FoodDatabase:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = self.load_data()
        self.similarity_matrix = None
        self._build_similarity_matrix()
    
    def load_data(self):
        """Load food database from CSV"""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Food database not found at {self.csv_path}")
        
        df = pd.read_csv(self.csv_path)
        print(f"DEBUG: Loaded {len(df)} foods from database")
        return df
    
    def _build_similarity_matrix(self):
        """Build similarity matrix for recommendations"""
        # Select nutritional features for similarity calculation
        nutritional_features = ['calories', 'protein', 'fat', 'carbs', 'fiber']
        
        # Check if features exist
        for feature in nutritional_features:
            if feature not in self.df.columns:
                print(f"Warning: Feature {feature} not in database")
                return
        
        # Extract and scale features
        feature_matrix = self.df[nutritional_features].fillna(0).values
        
        # Scale features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(feature_matrix)
        
        # Calculate cosine similarity
        self.similarity_matrix = cosine_similarity(scaled_features)
        print("DEBUG: Built similarity matrix for recommendations")
    
    def search_food(self, query, top_n=10):
        """Search for food by name"""
        if not query:
            return []
        
        query_lower = query.lower()
        
        # Find exact matches first
        exact_matches = self.df[self.df['name'].str.lower() == query_lower]
        
        if not exact_matches.empty:
            return exact_matches.head(top_n).to_dict('records')
        
        # Find partial matches
        partial_matches = self.df[self.df['name'].str.contains(query, case=False, na=False)]
        
        if not partial_matches.empty:
            return partial_matches.head(top_n).to_dict('records')
        
        return []
    
    def get_recommendations(self, food_name, top_n=5):
        """Get food recommendations based on nutritional similarity"""
        print(f"DEBUG: Getting recommendations for: {food_name}")
        
        # Find the food index
        food_idx = None
        for idx, row in self.df.iterrows():
            if str(row['name']).lower() == food_name.lower():
                food_idx = idx
                break
        
        if food_idx is None:
            print(f"DEBUG: Food '{food_name}' not found in database")
            # Try partial match
            for idx, row in self.df.iterrows():
                if food_name.lower() in str(row['name']).lower():
                    food_idx = idx
                    break
        
        if food_idx is None or self.similarity_matrix is None:
            print(f"DEBUG: No recommendations available for {food_name}")
            # Fallback: return random foods from same category
            return self.get_fallback_recommendations(food_name, top_n)
        
        # Get similarity scores
        similarities = self.similarity_matrix[food_idx]
        
        # Get top N most similar foods (excluding the food itself)
        similar_indices = similarities.argsort()[::-1][1:top_n+1]
        
        recommendations = []
        for idx in similar_indices:
            food = self.df.iloc[idx].to_dict()
            recommendations.append(food)
        
        print(f"DEBUG: Found {len(recommendations)} recommendations")
        return recommendations
    
    def get_fallback_recommendations(self, food_name, top_n=5):
        """Fallback recommendation method"""
        # Try to get category of the food
        food_entry = None
        for _, row in self.df.iterrows():
            if food_name.lower() in str(row['name']).lower():
                food_entry = row
                break
        
        if food_entry is not None and 'category' in self.df.columns:
            category = food_entry['category']
            # Get other foods from same category
            same_category = self.df[
                (self.df['category'] == category) & 
                (self.df['name'].str.lower() != food_name.lower())
            ]
            
            if not same_category.empty:
                return same_category.head(top_n).to_dict('records')
        
        # If still nothing, return random foods
        return self.df.sample(min(top_n, len(self.df))).to_dict('records')
    
    def calculate_nutrition(self, food_list):
        """Calculate total nutrition for a list of foods"""
        total_nutrition = {
            'calories': 0,
            'protein': 0,
            'fat': 0,
            'carbs': 0,
            'fiber': 0,
            'sugar': 0
        }
        
        for food_item in food_list:
            food_name = food_item['name']
            quantity = food_item.get('quantity', 1)
            
            # Find the food in database
            food_data = None
            for _, row in self.df.iterrows():
                if str(row['name']).lower() == food_name.lower():
                    food_data = row
                    break
            
            if food_data is not None:
                total_nutrition['calories'] += food_data['calories'] * quantity
                total_nutrition['protein'] += food_data['protein'] * quantity
                total_nutrition['fat'] += food_data['fat'] * quantity
                total_nutrition['carbs'] += food_data['carbs'] * quantity
                total_nutrition['fiber'] += food_data.get('fiber', 0) * quantity
                total_nutrition['sugar'] += food_data.get('sugar', 0) * quantity
        
        # Round to reasonable precision
        for key in total_nutrition:
            total_nutrition[key] = round(total_nutrition[key], 1)
        
        return total_nutrition
import random
import json

class FoodRecommender:
    def __init__(self):
        self.food_db = {
            'joy': [
                {'name': '🎉 Celebration Cake', 'type': 'dessert', 'cuisine': 'American', 'prep_time': '45 mins', 'difficulty': 'Medium', 'calories': 450},
                {'name': '🌈 Rainbow Pasta Salad', 'type': 'salad', 'cuisine': 'Italian', 'prep_time': '20 mins', 'difficulty': 'Easy', 'calories': 320},
                {'name': '🍣 Sushi Party Platter', 'type': 'main', 'cuisine': 'Japanese', 'prep_time': '60 mins', 'difficulty': 'Hard', 'calories': 380},
                {'name': '🍕 Fun Pizza', 'type': 'main', 'cuisine': 'Italian', 'prep_time': '30 mins', 'difficulty': 'Easy', 'calories': 550},
                {'name': '🍦 Ice Cream Sundae', 'type': 'dessert', 'cuisine': 'American', 'prep_time': '10 mins', 'difficulty': 'Easy', 'calories': 380}
            ],
            'sadness': [
                {'name': '🫕 Mac and Cheese', 'type': 'main', 'cuisine': 'American', 'prep_time': '25 mins', 'difficulty': 'Easy', 'calories': 480},
                {'name': '🍫 Warm Chocolate Pudding', 'type': 'dessert', 'cuisine': 'French', 'prep_time': '30 mins', 'difficulty': 'Medium', 'calories': 420},
                {'name': '🍲 Chicken Noodle Soup', 'type': 'soup', 'cuisine': 'American', 'prep_time': '40 mins', 'difficulty': 'Easy', 'calories': 280},
                {'name': '🥔 Mashed Potatoes', 'type': 'side', 'cuisine': 'American', 'prep_time': '20 mins', 'difficulty': 'Easy', 'calories': 250},
                {'name': '🍞 Grilled Cheese', 'type': 'sandwich', 'cuisine': 'American', 'prep_time': '10 mins', 'difficulty': 'Easy', 'calories': 350}
            ],
            'love': [
                {'name': '🍓 Chocolate Strawberries', 'type': 'dessert', 'cuisine': 'French', 'prep_time': '15 mins', 'difficulty': 'Easy', 'calories': 220},
                {'name': '❤️ Heart-shaped Pizza', 'type': 'main', 'cuisine': 'Italian', 'prep_time': '35 mins', 'difficulty': 'Medium', 'calories': 580},
                {'name': '🍝 Romantic Pasta', 'type': 'main', 'cuisine': 'Italian', 'prep_time': '25 mins', 'difficulty': 'Medium', 'calories': 420},
                {'name': '🍷 Wine Pairing', 'type': 'beverage', 'cuisine': 'French', 'prep_time': '5 mins', 'difficulty': 'Easy', 'calories': 150},
                {'name': '🍰 Tiramisu', 'type': 'dessert', 'cuisine': 'Italian', 'prep_time': '45 mins', 'difficulty': 'Medium', 'calories': 380}
            ],
            'anger': [
                {'name': '🌶️ Spicy Chicken Wings', 'type': 'appetizer', 'cuisine': 'American', 'prep_time': '40 mins', 'difficulty': 'Medium', 'calories': 520},
                {'name': '🔥 Ghost Pepper Chili', 'type': 'main', 'cuisine': 'Mexican', 'prep_time': '50 mins', 'difficulty': 'Hard', 'calories': 480},
                {'name': '🌮 Spicy Tacos', 'type': 'main', 'cuisine': 'Mexican', 'prep_time': '30 mins', 'difficulty': 'Medium', 'calories': 450},
                {'name': '🍛 Vindaloo Curry', 'type': 'main', 'cuisine': 'Indian', 'prep_time': '60 mins', 'difficulty': 'Hard', 'calories': 520},
                {'name': '🌶️ Spicy Ramen', 'type': 'main', 'cuisine': 'Japanese', 'prep_time': '25 mins', 'difficulty': 'Medium', 'calories': 480}
            ],
            'fear': [
                {'name': '🫕 Warm Soup', 'type': 'soup', 'cuisine': 'Various', 'prep_time': '25 mins', 'difficulty': 'Easy', 'calories': 180},
                {'name': '🍵 Chamomile Tea', 'type': 'beverage', 'cuisine': 'Various', 'prep_time': '5 mins', 'difficulty': 'Easy', 'calories': 50},
                {'name': '🥛 Warm Milk', 'type': 'beverage', 'cuisine': 'Various', 'prep_time': '5 mins', 'difficulty': 'Easy', 'calories': 120},
                {'name': '🍚 Rice Pudding', 'type': 'dessert', 'cuisine': 'British', 'prep_time': '40 mins', 'difficulty': 'Easy', 'calories': 250},
                {'name': '🍎 Baked Apple', 'type': 'dessert', 'cuisine': 'American', 'prep_time': '30 mins', 'difficulty': 'Easy', 'calories': 180}
            ],
            'surprise': [
                {'name': '🎲 Mystery Box', 'type': 'surprise', 'cuisine': 'International', 'prep_time': 'varies', 'difficulty': 'Fun', 'calories': 'varies'},
                {'name': '🍣 Sushi Burrito', 'type': 'fusion', 'cuisine': 'Japanese-Mexican', 'prep_time': '30 mins', 'difficulty': 'Medium', 'calories': 520},
                {'name': '🍔 Donut Burger', 'type': 'fusion', 'cuisine': 'American', 'prep_time': '25 mins', 'difficulty': 'Medium', 'calories': 680},
                {'name': '🍦 Fried Ice Cream', 'type': 'dessert', 'cuisine': 'Mexican', 'prep_time': '20 mins', 'difficulty': 'Hard', 'calories': 420},
                {'name': '🎂 Surprise Cake', 'type': 'dessert', 'cuisine': 'Various', 'prep_time': '50 mins', 'difficulty': 'Medium', 'calories': 450}
            ]
        }
    
    def get_food_recommendations(self, mood, limit=3):
        if mood not in self.food_db:
            mood = 'joy'
        foods = self.food_db[mood].copy()
        random.shuffle(foods)
        return foods[:limit]
    
    def get_recipe_details(self, food_name):
        for mood_category in self.food_db.values():
            for food in mood_category:
                if food_name.lower() in food['name'].lower():
                    return {
                        'name': food['name'],
                        'type': food['type'],
                        'cuisine': food['cuisine'],
                        'prep_time': food.get('prep_time', '30 mins'),
                        'difficulty': food.get('difficulty', 'Medium'),
                        'calories': food.get('calories', 'N/A'),
                        'ingredients': self._get_ingredients(food['name']),
                        'instructions': self._get_instructions(food['name'])
                    }
        return None
    
    def _get_ingredients(self, food_name):
        ingredients_map = {
            'Celebration Cake': ['flour', 'sugar', 'eggs', 'butter', 'vanilla', 'sprinkles'],
            'Mac and Cheese': ['pasta', 'cheddar cheese', 'milk', 'butter', 'breadcrumbs'],
            'Chocolate Strawberries': ['strawberries', 'dark chocolate', 'white chocolate'],
            'Spicy Wings': ['chicken wings', 'hot sauce', 'butter', 'garlic powder']
        }
        return ingredients_map.get(food_name, ['Check recipe for complete ingredients'])
    
    def _get_instructions(self, food_name):
        return f"Step by step instructions for {food_name}. Combine ingredients and cook with love!"

print("✅ Food Recommender created!")

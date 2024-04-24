import requests
import random

class MealRatingSystem:
    def __init__(self, meal_id=None, meal_name=None):
        self.meal_id = meal_id
        self.meal_name = meal_name
        self.ratings = self.generate_random_ratings() if meal_id else []

    def fetch_meal_data(self, meal_name):
        """Fetch meal data from TheMealDB API based on the meal name."""
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
        response = requests.get(url)
        data = response.json()
        
        if data['meals']:
            meal_info = data['meals'][0]
            self.meal_id = meal_info['idMeal']
            self.meal_name = meal_info['strMeal']
            self.ratings = self.generate_random_ratings()
        else:
            raise ValueError(f"No meal found with the name {meal_name}")

    def generate_random_ratings(self, num_ratings=20, rating_scale=(1, 6)):
        """Generate random ratings for the meal."""
        random.seed(self.meal_id)  # Use meal_id as the seed for reproducibility
        ratings = [random.randint(*rating_scale) for _ in range(num_ratings)]
        return ratings

    def add_user_rating_to_list(self, user_rating):
        """Add a user rating to the list and calculate the new average for the meal."""
        self.ratings.append(user_rating)
        # Calculate the new average rating
        new_average = round(sum(self.ratings) / len(self.ratings), 1)
        return new_average

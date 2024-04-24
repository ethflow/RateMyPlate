import requests
import random

class MealRatingSystem:
    # Dictionary to store ratings for each meal ID
    ratings_dict = {}

    def __init__(self, meal_id=None, meal_name=None):
        self.meal_id = meal_id
        self.meal_name = meal_name

        # If the meal ID exists in the dictionary, use the existing ratings list
        if meal_id in MealRatingSystem.ratings_dict:
            self.ratings = MealRatingSystem.ratings_dict[meal_id]
        else:
            # Otherwise, generate new random ratings and store them in the dictionary
            self.ratings = self.generate_random_ratings() if meal_id else []
            MealRatingSystem.ratings_dict[meal_id] = self.ratings

    def fetch_meal_data(self, meal_name):
        """Fetch meal data from TheMealDB API based on the meal name."""
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
        response = requests.get(url)
        data = response.json()

        if data['meals']:
            meal_info = data['meals'][0]
            self.meal_id = meal_info['idMeal']
            self.meal_name = meal_info['strMeal']

            # Use the existing ratings list if available, or generate new ratings
            if self.meal_id in MealRatingSystem.ratings_dict:
                self.ratings = MealRatingSystem.ratings_dict[self.meal_id]
            else:
                self.ratings = self.generate_random_ratings()
                MealRatingSystem.ratings_dict[self.meal_id] = self.ratings
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
        # Store the updated ratings list in the dictionary
        MealRatingSystem.ratings_dict[self.meal_id] = self.ratings
        
        # Calculate the new average rating
        new_average = round(sum(self.ratings) / len(self.ratings), 1)
        return new_average

import requests
import random

# Handle the rating of meals
class MealRatingSystem:
    # Dictionary to store ratings for each meal ID
    ratings_dict = {}

    # Constructor, initialize with given meal ID and name
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

    # Fetch meal data from API based on meal name
    def fetch_meal_data(self, meal_name):
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
        response = requests.get(url)
        data = response.json()

        # If meal is found, extract meal ID and name
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
            raise ValueError(f"Kein Gericht mit dem Namen {meal_name} gefunden")

    # Generate random ratings for the meal, N = 20, scale 1-6
    def generate_random_ratings(self, num_ratings=20, rating_scale=(1, 6)):
        # Use meal_id as the seed for reproducibility, https://www.w3schools.com/python/ref_random_seed.asp
        random.seed(self.meal_id)  
        ratings = [random.randint(*rating_scale) for _ in range(num_ratings)]
        return ratings

    # Add user rating to rating list and calculate new average for the meal
    def add_user_rating_to_list(self, user_rating):
        # Check if user rating is valid
        if 1 <= user_rating <= 6:
            self.ratings.append(user_rating)

            # Store the updated ratings list in the dictionary
            MealRatingSystem.ratings_dict[self.meal_id] = self.ratings
            
            # Calculate the new average rating
            new_average = round(sum(self.ratings) / len(self.ratings), 1)
            return new_average
        else:
            return None
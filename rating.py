import requests
import random
import os

class MealRatingSystem:
    def __init__(self, meal_id):
        self.meal_id = meal_id
        self.filename = f"ratings_{self.meal_id}.txt"
        self.ratings = self.load_existing_ratings()  # Load existing ratings on initialization

    def fetch_meal_data(self):
        """Fetch meal data from TheMealDB API based on the given meal ID."""
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={self.meal_id}"
        response = requests.get(url)
        data = response.json()
        return data

    def extract_meal_info(self, data):
        """Extract meal ID and meal name from the API response."""
        meals = data['meals'][0]
        self.meal_name = meals['strMeal']
        return self.meal_id, self.meal_name

    def generate_consistent_ratings(self, num_ratings=50, rating_scale=(1, 6)):
        """Generate consistent ratings using a deterministic random seed."""
        random.seed(int(self.meal_id))
        ratings = [random.randint(*rating_scale) for _ in range(num_ratings)]
        return ratings

    def load_existing_ratings(self):
        """Load existing ratings from a file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return [int(line.strip()) for line in file]
        else:
            # If no existing ratings, generate initial ratings
            initial_ratings = self.generate_consistent_ratings()
            self.save_ratings(initial_ratings)
            return initial_ratings

    def save_ratings(self, ratings):
        """Save ratings to a file."""
        with open(self.filename, 'w') as file:
            file.writelines(f"{rating}\n" for rating in ratings)

    def request_user_rating(self):
        """Prompt the user for a rating between 1 and 6 using Streamlit."""
        # Use Streamlit's number_input for user rating input
        user_rating = st.number_input(
            "Bewerten Sie Ihr Gericht von 1 bis 6:", min_value=1, max_value=6, step=1)
        return user_rating

    def add_user_rating_to_list(self, user_rating):
        """Add user rating to the existing list of ratings and calculate the new average."""
        self.ratings.append(user_rating)
        new_average = round(sum(self.ratings) / len(self.ratings), 1)
        self.save_ratings(self.ratings)
        return new_average

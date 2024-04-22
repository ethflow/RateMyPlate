import requests
import random
import os

class MealRatingSystem:
    def __init__(self, meal_id):
        self.meal_id = meal_id
        self.filename = f"ratings_{self.meal_id}.txt"

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
        """Generate a consistent list of ratings for a given meal ID using a deterministic random seed."""
        random.seed(int(self.meal_id))  # Convert meal_id to integer for seeding
        ratings = [random.randint(*rating_scale) for _ in range(num_ratings)]
        return ratings

    def load_existing_ratings(self):
        """Load existing ratings from a file."""
        try:
            with open(self.filename, 'r') as file:
                ratings = [int(line.strip()) for line in file.readlines()]
            return ratings
        except FileNotFoundError:
            return []

    def save_ratings(self, ratings):
        """Save ratings to a file."""
        with open(self.filename, 'w') as file:
            for rating in ratings:
                file.write(f"{rating}\n")

    def request_user_rating(self):
        """Prompt the user for a rating between 1 and 6. Ensure the rating is valid and handle different input types."""
        while True:
            user_input = input("Schön warst du Gast bei uns :-) bewerte dein Gericht von 1 bis 6: ")
            try:
                user_rating = int(user_input)
                if 1 <= user_rating <= 6:
                    break
                else:
                    print("Bitte bewerte dein Gericht mit einer Zahl von 1 bis 6")
            except ValueError:
                print("Bitte bewerte dein Gericht mit einer ganzen Zahl von 1 bis 6")
        return user_rating

    def add_user_rating_to_list(self, ratings, user_rating):
        """Add user rating to the existing list of ratings and calculate the new average."""
        ratings.append(user_rating)
        new_average = round(sum(ratings) / len(ratings), 1)  # Rounding to one decimal place
        return new_average

    def run(self):
        """Main function to handle API data fetching, initial rating generation, user rating addition, and final output."""
        meal_data = self.fetch_meal_data()
        meal_id, meal_name = self.extract_meal_info(meal_data)

        initial_ratings = self.load_existing_ratings()
        if not initial_ratings:
            initial_ratings = self.generate_consistent_ratings()
            self.save_ratings(initial_ratings)

        user_rating = self.request_user_rating()
        new_average = self.add_user_rating_to_list(initial_ratings, user_rating)
        self.save_ratings(initial_ratings)

        #print(f"Meal ID: {meal_id}, Meal Name: {meal_name}")
        #print(f"Updated Ratings: {initial_ratings}")
        #print(f"New Average Rating: {new_average}")

# Example of using the class
system = MealRatingSystem("52779")
system.run()

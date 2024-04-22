import requests
import random

def fetch_meal_data(meal_id):
    """Fetch meal data from TheMealDB API based on the given meal ID."""
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    response = requests.get(url)
    data = response.json()
    return data

def extract_meal_info(data):
    """Extract meal ID and meal name from the API response."""
    meals = data['meals'][0]  # Assuming the response contains at least one meal
    meal_id = meals['idMeal']
    meal_name = meals['strMeal']
    return meal_id, meal_name

def generate_consistent_ratings(meal_id, num_ratings=50, rating_scale=(1, 6)):
    """Generate a consistent list of ratings for a given meal ID using a deterministic random seed."""
    random.seed(meal_id)
    ratings = [random.randint(*rating_scale) for _ in range(num_ratings)]
    return ratings

def load_existing_ratings(filename):
    """Load existing ratings from a file."""
    try:
        with open(filename, 'r') as file:
            ratings = [int(line.strip()) for line in file.readlines()]
        return ratings
    except FileNotFoundError:
        return []

def save_ratings(filename, ratings):
    """Save ratings to a file."""
    with open(filename, 'w') as file:
        for rating in ratings:
            file.write(f"{rating}\n")

def request_user_rating():
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

def add_user_rating_to_list(ratings, user_rating):
    """Add user rating to the existing list of ratings and calculate the new average."""
    ratings.append(user_rating)
    new_average = round(sum(ratings) / len(ratings), 2)
    return new_average

def main_with_user_interaction(meal_id, filename='ratings.txt'):
    """Main function to handle API data fetching, initial rating generation, user rating addition, and final output."""
    meal_data = fetch_meal_data(meal_id)
    meal_id, meal_name = extract_meal_info(meal_data)
    initial_ratings = load_existing_ratings(filename)
    if not initial_ratings:
        initial_ratings = generate_consistent_ratings(meal_id)

    # Request user rating and update the ratings list
    user_rating = request_user_rating()
    new_average = add_user_rating_to_list(initial_ratings, user_rating)
    save_ratings(filename, initial_ratings)

    print(f"Meal ID: {meal_id}, Meal Name: {meal_name}")
    print(f"Updated Ratings: {initial_ratings}")
    print(f"New Average Rating: {new_average}")

# You can call the main function with a specific meal ID, like this:
main_with_user_interaction("52772")

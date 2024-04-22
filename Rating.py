import requests
import json

def fetch_all_meals():
    # Base URL for fetching meals by first letter
    base_url = "https://www.themealdb.com/api/json/v1/1/search.php?f={}"
    all_meals = []  # List to store all meals

    # Loop through each letter in the alphabet
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        # Format the URL with the current letter
        url = base_url.format(letter)

        # Send GET request to the API
        response = requests.get(url)

        # Parse JSON response
        data = response.json()

        # Check if there are any meals for the letter
        if data['meals'] is not None:
            # Add meals to the list
            all_meals.extend(meal['strMeal'] for meal in data['meals'])

    # Print all collected meals
    print("All meals collected from the API:")
    for meal in all_meals:
        print(meal)

fetch_all_meals()



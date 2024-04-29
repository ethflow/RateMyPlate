import requests
import random

# Class to generate a weekly menu
class WeeklyMenuGenerator:
    # Constructor
    def __init__(self):
        self.weekly_menu = []
        self.veg_menu = self.generate_vegetarian_menu()
        self.non_veg_menu = self.generate_non_vegetarian_menu()
        self.grouped_menu = self.group_meals_by_day()

    # Generate a list of vegetarian meals
    def generate_vegetarian_menu(self):
        veg_menu = []
        # Store unique meal IDs and avoid duplicates
        meal_ids_set = set()
        # API URL
        url = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=vegetarian'

        # Fetch until the set contains 5 unique meals
        while len(veg_menu) < 5:
            new_meal = self.fetch_random_meal(url)
            
            # If API request fails, skip current iteration of the loop
            if new_meal is None:
                continue
            
            meal_id, meal_name, meal_thumb = new_meal
            
            # Check if the meal ID is unique and add it to the menu
            if meal_id not in meal_ids_set:
                meal_ids_set.add(meal_id)
                veg_menu.append(new_meal)
        
        return veg_menu

    def generate_non_vegetarian_menu(self):
        # Non-vegetarian categories and URLs
        categories = {
            'chicken': 'https://www.themealdb.com/api/json/v1/1/filter.php?c=chicken',
            'pasta': 'https://www.themealdb.com/api/json/v1/1/filter.php?c=pasta',
            'beef': 'https://www.themealdb.com/api/json/v1/1/filter.php?c=beef',
            'seafood': 'https://www.themealdb.com/api/json/v1/1/filter.php?c=seafood',
            'pork': 'https://www.themealdb.com/api/json/v1/1/filter.php?c=pork',
        }
        
        non_veg_menu = []
        
        # Fetch a random meal for each category
        for category, url in categories.items():
            meal = self.fetch_random_meal(url)
            if meal is not None:
                non_veg_menu.append(meal)
        
        return non_veg_menu

    # Fetch a random meal from the API
    def fetch_random_meal(self, url):
        response = requests.get(url)
        data = response.json()
        meals_list = data.get('meals', [])

        # If there are no meals in the response, return None
        if not meals_list:
            return None

        # Choose a random index from the list of meals
        i = random.randint(0, len(meals_list) - 1)

        # Get meal information from the random index
        meal_id = meals_list[i].get('idMeal')
        meal_name = meals_list[i].get('strMeal')
        meal_thumb = meals_list[i].get('strMealThumb')

        # Return the meal information as a tuple
        return (meal_id, meal_name, meal_thumb)

    # Group vegetarian and non-vegetarian meals by day of the week
    def group_meals_by_day(self):
        grouped_menu = []

        # Zip the vegetarian and non-vegetarian menus
        paired_meals = zip(self.veg_menu, self.non_veg_menu)

        # Iterate over the paired meals, enumerate: https://www.geeksforgeeks.org/enumerate-in-python/
        for day, (veg_meal, non_veg_meal) in enumerate(paired_meals, start=1):
            # Create a tuple with the vegetarian and non-vegetarian meal
            grouped_menu.append((veg_meal, non_veg_meal))

        return grouped_menu
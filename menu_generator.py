import requests
import random

class WeeklyMenuGenerator:
    def __init__(self):
        # Cache the meals data to reduce API calls
        self.meals_cache = {}
        self.grouped_menu = self.generate_weekly_menu()

    def fetch_meals(self, category):
        # Check the cache first
        if category in self.meals_cache:
            return self.meals_cache[category]

        # Fetch meals from API and cache the result
        url = f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}'
        response = requests.get(url)
        data = response.json()
        meals_list = data.get('meals', [])
        
        # Cache the result for future use
        self.meals_cache[category] = meals_list
        return meals_list

    def generate_weekly_menu(self):
        categories = ['vegetarian', 'chicken', 'pasta', 'beef', 'seafood', 'pork']
        weekly_menu = []
        random.seed()

        # For each category, fetch a random meal
        for category in categories:
            meals_list = self.fetch_meals(category)
            if meals_list:
                random_meal = random.choice(meals_list)
                weekly_menu.append(random_meal)
        
        # Pair each vegetarian meal with one non-vegetarian meal for each weekday
        paired_menu = list(zip(weekly_menu[0:1], weekly_menu[1:]))
        return paired_menu

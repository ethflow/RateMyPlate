import requests
import json
import random

weekly_menu = []

# Initialize a list for the weekly menu
veg_menu = []

# Create a set to track unique meal identifiers
meal_ids_set = set()

# Define the function to look up vegetarian meals
def meal_lookup_veg():
    url = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=vegetarian'
    
    response = requests.get(url)
    data = response.json()
    meals_list = data.get('meals', [])
    
    if not meals_list:
        # If there are no meals in the response, return None
        return None
    
    # Choose a random index from the list of meals
    i = random.randint(0, len(meals_list) - 1)
    
    # Get meal information from the random index
    meal_id = meals_list[i]['idMeal']
    meal_name = meals_list[i]['strMeal']
    
    # Return the meal information as a tuple
    return (meal_id, meal_name)

# Continue adding meals until we have 5 unique meals in the weekly menu
while len(veg_menu) < 5:
    new_meal = meal_lookup_veg()
    
    if new_meal is None:
        continue
    
    # Unpack the meal information
    meal_id, meal_name = new_meal
    
    # Check if the meal ID is already in the set
    if meal_id not in meal_ids_set:
        # If the meal ID is unique, add it to the set and the weekly menu
        meal_ids_set.add(meal_id)
        veg_menu.append(new_meal)

weekly_menu.append(veg_menu)

def meal_lookup():
    url_ch = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=chicken'
    url_pa = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=pasta'
    url_be = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=beef'
    url_se = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=seafood'
    url_po = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=pork'

    #Chicken
    response_ch = requests.get(url_ch)
    data_ch = response_ch.json()
    meals_list_ch = data_ch.get('meals', [])
    i = random.randint(0, len(meals_list_ch) - 1)
    meal_id_ch = meals_list_ch[i]['idMeal']
    meal_name_ch = meals_list_ch[i]['strMeal']
    meal_ch = (meal_id_ch, meal_name_ch)

    #Pasta
    response_pa = requests.get(url_pa)
    data_pa = response_pa.json()
    meals_list_pa = data_pa.get('meals', [])
    i = random.randint(0, len(meals_list_pa) - 1)
    meal_id_pa = meals_list_pa[i]['idMeal']
    meal_name_pa = meals_list_pa[i]['strMeal']
    meal_pa = (meal_id_pa, meal_name_pa)

    #Beef
    response_be = requests.get(url_be)
    data_be = response_be.json()
    meals_list_be = data_be.get('meals', [])
    i = random.randint(0, len(meals_list_be) - 1)
    meal_id_be = meals_list_be[i]['idMeal']
    meal_name_be = meals_list_be[i]['strMeal']
    meal_be = (meal_id_be, meal_name_be)

    #Seafood
    response_se = requests.get(url_se)
    data_se = response_se.json()
    meals_list_se = data_se.get('meals', [])
    i = random.randint(0, len(meals_list_se) - 1)
    meal_id_se = meals_list_se[i]['idMeal']
    meal_name_se = meals_list_se[i]['strMeal']
    meal_se = (meal_id_se, meal_name_se)

    #Pork
    response_po = requests.get(url_po)
    data_po = response_po.json()
    meals_list_po = data_po.get('meals', [])
    i = random.randint(0, len(meals_list_po) - 1)
    meal_id_po = meals_list_po[i]['idMeal']
    meal_name_po = meals_list_po[i]['strMeal']
    meal_po = (meal_id_po, meal_name_po)
    
    # Return the meal information as a tuple
    return [meal_ch, meal_pa, meal_be, meal_se, meal_po]

weekly_menu.append(meal_lookup())

weekly_menu




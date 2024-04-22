import streamlit as st
from menu_generator import WeeklyMenuGenerator
from rating import MealRatingSystem

# Title of the application
st.title("Wochenplan")

# Initialize the menu generator and rating systems as session state variables to persist across reruns
if 'menu_generator' not in st.session_state:
    st.session_state.menu_generator = WeeklyMenuGenerator()
if 'rating_systems' not in st.session_state:
    st.session_state.rating_systems = {}

# Function to generate a new weekly menu and initialize the rating systems for each meal
def generate_new_weekly_menu():
    # Generate a new instance of the WeeklyMenuGenerator class
    st.session_state.menu_generator = WeeklyMenuGenerator()
    # Initialize rating systems for the new menu
    grouped_menu = st.session_state.menu_generator.grouped_menu
    initialize_rating_systems(grouped_menu)
    return grouped_menu

# Function to initialize MealRatingSystem objects for each meal in the weekly menu
def initialize_rating_systems(grouped_menu):
    for day, meals in zip(days_of_week, grouped_menu):
        veg_meal, non_veg_meal = meals
        for meal in [veg_meal, non_veg_meal]:
            meal_id = meal[0]
            if meal_id not in st.session_state.rating_systems:
                st.session_state.rating_systems[meal_id] = MealRatingSystem(meal_id)

# Add a button that generates a new weekly menu when clicked
if st.button("Nächste Woche"):
    grouped_menu = generate_new_weekly_menu()
else:
    # Use the existing menu if the button has not been clicked
    grouped_menu = st.session_state.menu_generator.grouped_menu
    initialize_rating_systems(grouped_menu)


# Display the grouped weekly menu for Monday to Friday and allow user ratings
# Iterate through the days of the week and the grouped meals
days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
for day, meals in zip(days_of_week, grouped_menu):
    veg_meal, non_veg_meal = meals
    st.subheader(day)

    # Display meal names for vegetarian and non-vegetarian meals
    st.text(f"Vegetarisch: {veg_meal[1]}")
    st.text(f"Nicht-vegetarisch: {non_veg_meal[1]}")

    # Get the meal IDs for the vegetarian and non-vegetarian meals
    veg_meal_id = veg_meal[0]
    non_veg_meal_id = non_veg_meal[0]

    # Create rating objects for vegetarian and non-vegetarian meals
    if veg_meal_id not in st.session_state:
        st.session_state[veg_meal_id] = MealRatingSystem(veg_meal_id)
    if non_veg_meal_id not in st.session_state:
        st.session_state[non_veg_meal_id] = MealRatingSystem(non_veg_meal_id)

    # Get the rating objects from session state
    veg_rating_system = st.session_state[veg_meal_id]
    non_veg_rating_system = st.session_state[non_veg_meal_id]

    # Prompt the user for a rating using the request_user_rating function
    # for the vegetarian meal
    veg_user_rating = st.number_input(
        "Bewerten Sie Ihr vegetarisches Gericht von 1 bis 6:",
        min_value=1, max_value=6, step=1, key=f"veg_{veg_meal_id}"
    )
    veg_new_average = veg_rating_system.add_user_rating_to_list(
        veg_rating_system.load_existing_ratings(), veg_user_rating
    )
    veg_rating_system.save_ratings(veg_rating_system.load_existing_ratings())

    # Display the new average rating for vegetarian meal
    st.text(f"Durchschnittliche Bewertung Vegetarisch: {veg_new_average}")

    # Prompt the user for a rating using the request_user_rating function
    # for the non-vegetarian meal
    non_veg_user_rating = st.number_input(
        "Bewerten Sie Ihr nicht-vegetarisches Gericht von 1 bis 6:",
        min_value=1, max_value=6, step=1, key=f"non_veg_{non_veg_meal_id}"
    )
    non_veg_new_average = non_veg_rating_system.add_user_rating_to_list(
        non_veg_rating_system.load_existing_ratings(), non_veg_user_rating
    )
    non_veg_rating_system.save_ratings(non_veg_rating_system.load_existing_ratings())

    # Display the new average rating for non-vegetarian meal
    st.text(f"Durchschnittliche Bewertung Nicht-vegetarisch: {non_veg_new_average}")


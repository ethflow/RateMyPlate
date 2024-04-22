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

# Define the days of the week
days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']

# Add a button that generates a new weekly menu when clicked
if st.button("Nächste Woche"):
    grouped_menu = generate_new_weekly_menu()
else:
    # Use the existing menu if the button has not been clicked
    grouped_menu = st.session_state.menu_generator.grouped_menu
    initialize_rating_systems(grouped_menu)

# Display the grouped weekly menu for Monday to Friday and allow user ratings
for day, meals in zip(days_of_week, grouped_menu):
    veg_meal, non_veg_meal = meals
    st.subheader(day)
    
    # Display the vegetarian meal and allow rating
    veg_meal_id, veg_meal_name = veg_meal
    st.text(f"Vegetarisch: {veg_meal_name}")
    if st.button(f"Rate {veg_meal_name}"):
        user_rating = st.session_state.rating_systems[veg_meal_id].request_user_rating()
        average_rating = st.session_state.rating_systems[veg_meal_id].add_user_rating_to_list(user_rating)
        st.text(f"Durchschnittliche Bewertung: {average_rating}")

    # Display the non-vegetarian meal and allow rating
    non_veg_meal_id, non_veg_meal_name = non_veg_meal
    st.text(f"Nicht-vegetarisch: {non_veg_meal_name}")
    if st.button(f"Rate {non_veg_meal_name}"):
        user_rating = st.session_state.rating_systems[non_veg_meal_id].request_user_rating()
        average_rating = st.session_state.rating_systems[non_veg_meal_id].add_user_rating_to_list(user_rating)
        st.text(f"Durchschnittliche Bewertung: {average_rating}")

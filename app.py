import streamlit as st
from menu_generator import WeeklyMenuGenerator
from rating import MealRatingSystem

# Application title
st.title("Wochenplan")

# Initialize the menu generator and rating systems as session state variables
if 'menu_generator' not in st.session_state:
    st.session_state.menu_generator = WeeklyMenuGenerator()

# Add a button to generate a new weekly menu
if st.button("Nächste Woche"):
    # Generate a new menu and initialize rating systems
    st.session_state.menu_generator = WeeklyMenuGenerator()
else:
    # Use the existing menu
    menu_generator = st.session_state.menu_generator

# Define the days of the week
days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']

# Initialize rating systems only once if they are not in session state
if 'rating_systems' not in st.session_state:
    st.session_state.rating_systems = {}
    for meals in menu_generator.grouped_menu:
        for meal in meals:
            meal_id = meal['idMeal']
            if meal_id not in st.session_state.rating_systems:
                st.session_state.rating_systems[meal_id] = MealRatingSystem(meal_id)

# Display weekly menu and allow rating for each meal
for day, meals in zip(days_of_week, menu_generator.grouped_menu):
    veg_meal, non_veg_meal = meals
    
    st.subheader(day)
    
    # Vegetarian meal
    st.text(f"Vegetarisch: {veg_meal['strMeal']}")
    # Allow rating for vegetarian meal
    veg_meal_id = veg_meal['idMeal']
    if st.button(f"Rate {veg_meal['strMeal']}"):
        rating_system = st.session_state.rating_systems[veg_meal_id]
        user_rating = rating_system.request_user_rating()
        avg_rating = rating_system.add_user_rating_to_list(user_rating)
        st.text(f"Durchschnittliche Bewertung: {avg_rating}")

    # Non-vegetarian meal
    st.text(f"Nicht-vegetarisch: {non_veg_meal['strMeal']}")
    # Allow rating for non-vegetarian meal
    non_veg_meal_id = non_veg_meal['idMeal']
    if st.button(f"Rate {non_veg_meal['strMeal']}"):
        rating_system = st.session_state.rating_systems[non_veg_meal_id]
        user_rating = rating_system.request_user_rating()
        avg_rating = rating_system.add_user_rating_to_list(user_rating)
        st.text(f"Durchschnittliche Bewertung: {avg_rating}")

import streamlit as st
import pandas as pd
from menu_generator import WeeklyMenuGenerator
from rating import MealRatingSystem

# Title of the application
st.title("Wochenplan")

# Initialize the menu generator as a session state variable to persist across reloads
if 'menu_generator' not in st.session_state:
    st.session_state.menu_generator = WeeklyMenuGenerator()

# Generate a new weekly menu when the button is clicked, or use the existing one
if st.button("Nächste Woche"):
    st.session_state.menu_generator = WeeklyMenuGenerator()
grouped_menu = st.session_state.menu_generator.grouped_menu

# Display the grouped weekly menu from Monday to Friday
days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
for day, meals in zip(days_of_week, grouped_menu):
    veg_meal, non_veg_meal = meals
    st.subheader(day)

    # Process each meal type (vegetarian and non-vegetarian)
    for meal in [veg_meal, non_veg_meal]:
        meal_id, meal_name = meal
        rating_system = MealRatingSystem(meal_id)

        # Display the meal name
        st.text(f"{meal_name}")

        # Input for new ratings using Streamlit
        user_rating = st.number_input("Bewerte dieses Gericht von 1 bis 6", min_value=1, max_value=6, step=1,
                                      key=f"{meal_id}_{day}")
        submit_button = st.button(f"Bewertung abgeben für {meal_name}", key=f"btn_{meal_id}_{day}")
        if submit_button:
            new_average_rating = rating_system.add_user_rating_to_list(user_rating)
            rating_system.save_ratings(rating_system.ratings)

        elif submit_button:
            st.error("Bitte bewerte dein Gericht mit einer Zahl von 1 bis 6")

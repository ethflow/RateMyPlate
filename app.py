import streamlit as st
from menu_generator import WeeklyMenuGenerator
from rating import MealRatingSystem

# Title of the application
st.title("Wochenplan")

# Create an instance of WeeklyMenuGenerator
# Initialize the menu generator as a session state variable to persist across reruns
if 'menu_generator' not in st.session_state:
    st.session_state.menu_generator = WeeklyMenuGenerator()


# Function to generate a new weekly menu
def generate_new_weekly_menu():
    st.session_state.menu_generator = WeeklyMenuGenerator()
    return st.session_state.menu_generator.grouped_menu


if st.button("Nächste Woche"):
    grouped_menu = generate_new_weekly_menu()
else:
    grouped_menu = st.session_state.menu_generator.grouped_menu

days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
for day, meals in zip(days_of_week, grouped_menu):
    veg_meal, non_veg_meal = meals
    st.subheader(day)

    # Vegetarian meal
    veg_meal_id = veg_meal[0]
    veg_meal_name = veg_meal[1]
    veg_rating_system = MealRatingSystem(veg_meal_id)
    veg_average_rating = round(sum(veg_rating_system.ratings) / len(veg_rating_system.ratings), 1)
    st.text(f"Vegetarisch: {veg_meal_name}")
    st.text(f"Durchschnittliche Bewertung: {veg_average_rating}")

    veg_user_rating = st.number_input(f"Bewerte das vegetarische Gericht '{veg_meal_name}' von 1 bis 6", min_value=1,
                                      max_value=6, step=1)
    if st.button(f"Bewertung abgeben für '{veg_meal_name}'"):
        new_average_rating = veg_rating_system.add_user_rating_to_list(veg_user_rating)
        st.bar_chart({'Average Rating': [new_average_rating]}, height=150)  # Ein Balken für die Durchschnittsbewertung

    # Non-vegetarian meal
    non_veg_meal_id = non_veg_meal[0]
    non_veg_meal_name = non_veg_meal[1]
    non_veg_rating_system = MealRatingSystem(non_veg_meal_id)
    non_veg_average_rating = round(sum(non_veg_rating_system.ratings) / len(non_veg_rating_system.ratings), 1)
    st.text(f"Nicht-vegetarisch: {non_veg_meal_name}")
    st.text(f"Durchschnittliche Bewertung: {non_veg_average_rating}")

    non_veg_user_rating = st.number_input(f"Bewerte das nicht-vegetarische Gericht '{non_veg_meal_name}' von 1 bis 6",
                                          min_value=1, max_value=6, step=1)
    if st.button(f"Bewertung abgeben für '{non_veg_meal_name}'"):
        new_average_rating = non_veg_rating_system.add_user_rating_to_list(non_veg_user_rating)
        st.bar_chart({'Average Rating': [new_average_rating]}, height=150)  # Ein Balken für die Durchschnittsbewertung

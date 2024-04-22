import streamlit as st
from menu_generator import WeeklyMenuGenerator
from rating import MealRatingSystem

# Title of the application
st.title("Wochenplan")

# Function to prompt the user for a rating using Streamlit
def request_user_rating():
    """Prompt the user for a rating between 1 and 6 using Streamlit."""
    return st.number_input("Bewerten Sie Ihr Gericht von 1 bis 6:", min_value=1, max_value=6, step=1)

# Initialize the menu generator as a session state variable to persist across reruns
if 'menu_generator' not in st.session_state:
    st.session_state.menu_generator = WeeklyMenuGenerator()

# Add a button that generates a new weekly menu when clicked
def generate_new_weekly_menu():
    st.session_state.menu_generator = WeeklyMenuGenerator()
    return st.session_state.menu_generator.grouped_menu

if st.button("Nächste Woche"):
    grouped_menu = generate_new_weekly_menu()
else:
    grouped_menu = st.session_state.menu_generator.grouped_menu

# Display the grouped weekly menu for Monday to Friday
days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
for day, meals in zip(days_of_week, grouped_menu):
    veg_meal, non_veg_meal = meals
    st.subheader(day)
    # Display meal names for vegetarian and non-vegetarian meals
    st.text(f"Vegetarisch: {veg_meal[1]}")
    st.text(f"Nicht-vegetarisch: {non_veg_meal[1]}")

    # Add rating functionality
    # Get the meal ID for the vegetarian and non-vegetarian meals
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

    # Prompt the user for a rating using the request_user_rating() function
    veg_user_rating = request_user_rating()
    non_veg_user_rating = request_user_rating()

    # Add the user ratings to the respective meals and calculate the new averages
    veg_new_average = veg_rating_system.add_user_rating_to_list(
        veg_rating_system.load_existing_ratings(), veg_user_rating)
    non_veg_new_average = non_veg_rating_system.add_user_rating_to_list(
        non_veg_rating_system.load_existing_ratings(), non_veg_user_rating)

    # Save the updated ratings
    veg_rating_system.save_ratings(veg_rating_system.load_existing_ratings())
    non_veg_rating_system.save_ratings(non_veg_rating_system.load_existing_ratings())

    # Display the new average ratings
    st.text(f"Durchschnittliche Bewertung Vegetarisch: {veg_new_average}")
    st.text(f"Durchschnittliche Bewertung Nicht-vegetarisch: {non_veg_new_average}")

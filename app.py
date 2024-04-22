import streamlit as st
from menu_generator import WeeklyMenuGenerator

# Title of the application
st.title("Wochenplan")

# Create an instance of WeeklyMenuGenerator
# Initialize the menu generator as a session state variable to persist across reruns
if 'menu_generator' not in st.session_state:
    st.session_state.menu_generator = WeeklyMenuGenerator()

# Function to generate a new weekly menu
def generate_new_weekly_menu():
    # Generate a new instance of the WeeklyMenuGenerator class
    st.session_state.menu_generator = WeeklyMenuGenerator()
    # Return the new grouped weekly menu
    return st.session_state.menu_generator.grouped_menu

# Add a button that generates a new weekly menu when clicked
if st.button("Nächste Woche"):
    grouped_menu = generate_new_weekly_menu()
else:
    # Use the existing menu if the button has not been clicked
    grouped_menu = st.session_state.menu_generator.grouped_menu

# Display the grouped weekly menu for Monday to Friday
days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
for day, meals in zip(days_of_week, grouped_menu):
    veg_meal, non_veg_meal = meals
    st.subheader(day)
    # Display only the meal names for vegetarian and non-vegetarian meals
    st.text(f"Vegetarisch: {veg_meal[1]}")
    st.text(f"Nicht-vegetarisch: {non_veg_meal[1]}")

import streamlit as st
from weeklymenugenerator import WeeklyMenuGenerator

# Title of the application
st.title("Weekly Menu Generator")

# Initialize the WeeklyMenuGenerator
menu_generator = WeeklyMenuGenerator()

# Display the grouped weekly menu for Monday to Friday
st.header("Grouped Weekly Menu (Monday to Friday):")
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
for day, meals in zip(days_of_week, menu_generator.grouped_menu):
    veg_meal, non_veg_meal = meals
    st.subheader(day)
    st.text(f"Vegetarian meal: {veg_meal[1]} (ID: {veg_meal[0]})")
    st.text(f"Non-vegetarian meal: {non_veg_meal[1]} (ID: {non_veg_meal[0]})")



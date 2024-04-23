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

    # For vegetarian meal
    veg_meal_id = veg_meal[0]
    veg_meal_name = veg_meal[1]
    veg_rating_system = MealRatingSystem(veg_meal_id)
    veg_average_rating = round(sum(veg_rating_system.ratings) / len(veg_rating_system.ratings), 1)

    # Display vegetarian meal name and average rating
    st.text(f"Vegetarisch: {veg_meal_name} (Durchschnittliche Bewertung: {veg_average_rating})")

    # Allow user to rate vegetarian meal
    veg_user_rating = st.number_input(f"Bewerte das vegetarische Gericht '{veg_meal_name}' von 1 bis 6", min_value=1,
                                      max_value=6, step=1, key=f'veg_{day}')
    if st.button(f"Bewertung abgeben für '{veg_meal_name}'", key=f'veg_btn_{day}'):
        new_average_rating = veg_rating_system.add_user_rating_to_list(veg_user_rating)
        # Update and display the new average rating
        st.bar_chart({'Rating': [1, new_average_rating, 6]})  # Visualized as a bar chart

    # For non-vegetarian meal
    non_veg_meal_id = non_veg_meal[0]
    non_veg_meal_name = non_veg_meal[1]
    non_veg_rating_system = MealRatingSystem(non_veg_meal_id)
    non_veg_average_rating = round(sum(non_veg_rating_system.ratings) / len(non_veg_rating_system.ratings), 1)

    # Display non-vegetarian meal name and average rating
    st.text(f"Nicht-vegetarisch: {non_veg_meal_name} (Durchschnittliche Bewertung: {non_veg_average_rating})")

    # Allow user to rate non-vegetarian meal
    non_veg_user_rating = st.number_input(f"Bewerte das nicht-vegetarische Gericht '{non_veg_meal_name}' von 1 bis 6",
                                          min_value=1, max_value=6, step=1, key=f'non_veg_{day}')
    if st.button(f"Bewertung abgeben für '{non_veg_meal_name}'", key=f'non_veg_btn_{day}'):
        new_average_rating = non_veg_rating_system.add_user_rating_to_list(non_veg_user_rating)
        # Update and display the new average rating
        st.bar_chart({'Rating': [1, new_average_rating, 6]})  # Visualized as a bar chart

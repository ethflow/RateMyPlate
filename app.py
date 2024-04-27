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

# Initialize lists to store meals and their average ratings
meal_names = []
average_ratings = []

# Display the grouped weekly menu from Monday to Friday
days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
# Initialize a counter for unique keys
rating_counter = 0

for day, meals in zip(days_of_week, grouped_menu):
    veg_meal, non_veg_meal = meals
    st.subheader(day)

    # Process each meal type (vegetarian and non-vegetarian)
    for meal in [veg_meal, non_veg_meal]:
        meal_id, meal_name = meal
        # Initialize MealRatingSystem for each meal
        rating_system = MealRatingSystem(meal_id=meal_id, meal_name=meal_name)

        # Display the meal name
        st.text(f"{meal_name}")

        # Generate a unique key for each rating and submit button by combining meal ID, day of the week, and the counter
        unique_key = f"{meal_id}_{day}_{rating_counter}"
        rating_counter += 1

        # Input for new ratings using Streamlit
        # Capture the user's input as a string using st.text_input
        user_input = st.text_input(f"Bewerte {meal_name} von 1 bis 6", key=unique_key)

        # Try to convert the input to an integer
        try:
            user_rating = int(user_input)
        except ValueError:
            user_rating = None  # If the input cannot be converted to an integer

        # Check if the input is within the valid range
        if user_rating is not None and 1 <= user_rating <= 6:
            # Display the user rating (optional)
            st.write(user_rating)
            # Button to submit the rating
            submit_button = st.button(f"Bewertung abgeben für {meal_name}", key=f"btn_{unique_key}")
            
            if submit_button:
                # Add user rating to the list and calculate the new average
                new_average_rating = rating_system.add_user_rating_to_list(user_rating)

                # Update the average rating display in the UI
                st.write(f"Neuer durchschnittlicher Bewertung für {meal_name}: {new_average_rating}")
        else:
            # Display an error message if the input is invalid
            st.error("Bitte geben Sie eine Bewertung von 1 bis 6 ein.")

        meal_names.append(meal_name)
        if rating_system.ratings:
            average_rating = round(sum(rating_system.ratings) / len(rating_system.ratings), 1)
        else:
            average_rating = 0
        average_ratings.append(average_rating)

# Create a DataFrame with the meal names and average ratings
data = pd.DataFrame({
    'Meal': meal_names,
    'Average Rating': average_ratings
})

# Visualize the average ratings at the end of the site
st.subheader("Durchschnittliche Bewertungen der Gerichte")
st.bar_chart(data.set_index('Meal'))

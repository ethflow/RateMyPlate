import streamlit as st
from menu_generator import WeeklyMenuGenerator
from rating import MealRatingSystem

# Title of the application
st.title("Wochenplan")

# Initialize the menu generator as a session state variable to persist across reruns
if 'menu_generator' not in st.session_state:
    st.session_state.menu_generator = WeeklyMenuGenerator()

# Generate a new weekly menu if the button is clicked or use the existing one
if st.button("Nächste Woche"):
    st.session_state.menu_generator = WeeklyMenuGenerator()
grouped_menu = st.session_state.menu_generator.grouped_menu

# Display the grouped weekly menu for Monday to Friday
days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
for day, meals in zip(days_of_week, grouped_menu):
    veg_meal, non_veg_meal = meals
    st.subheader(day)

    # Display and rate each meal type (vegetarian and non-vegetarian)
    for meal_id, meal_name in [veg_meal, non_veg_meal]:
        meal_type = "Vegetarisch" if meal_id == veg_meal[0] else "Nicht-vegetarisch"
        rating_system = MealRatingSystem(meal_id)
        average_rating = round(sum(rating_system.ratings) / len(rating_system.ratings), 1)

        # Display meal name and average rating
        st.write(f"{meal_type}: {meal_name} (Durchschnittliche Bewertung: {average_rating})")

        # Input for new rating
        user_rating = st.number_input("Bewerte dieses Gericht von 1 bis 6", min_value=1, max_value=6, step=1, key=f"{meal_id}")
        if st.button(f"Bewertung abgeben für {meal_name}", key=f"btn_{meal_id}"):
            new_average_rating = rating_system.add_user_rating_to_list(user_rating)
            rating_system.save_ratings(rating_system.ratings)
            st.write(f"Neue durchschnittliche Bewertung: {new_average_rating}")

            # Optional: Visualize the updated average as a bar chart
            st.bar_chart({'Rating': [1, new_average_rating, 6]})

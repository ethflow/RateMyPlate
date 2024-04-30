import streamlit as st
import pandas as pd
from menu_generator import WeeklyMenuGenerator
from rating import MealRatingSystem

# Title of the application
st.title("Willkommen bei RateMyPlate!")

# Description of the application
st.markdown("""

Mit dieser App können Sie jedes Gericht dieser Woche bewerten. Die Bewertung folgt einer Notenskala.
Auf Basis Ihres Feedbacks kann das wöchentliche Angebot der Mensa kontinuierlich verbessert werden!

**Anleitung zur Nutzung der App:**
- Sehen Sie sich den Wochenplan von Montag bis Freitag an, der täglich eine vegetarische und eine nicht-vegetarische Mahlzeit bietet.
- Um eine Mahlzeit zu bewerten, geben Sie eine Zahl von 1 bis 6 in das Eingabefeld unter dem Gericht ein.
- Nachdem Sie Ihre Bewertung eingegeben haben, klicken Sie auf den Button "Bewertung abgeben", um Ihre Bewertung abzusenden.
- Die App berechnet und zeigt die neue durchschnittliche Bewertung für die Mahlzeit an.
- Am Ende der Woche können Sie ein Balkendiagramm mit den durchschnittlichen Bewertungen aller Mahlzeiten im Menü sehen.
- Klicken Sie auf den Button "Nächste Woche", um den Wochenplan der nächsten Woche zu sehen.

Vielen Dank für Ihr Feedback!
""")

st.title("Wochenplan")

# Create a session state
if 'menu_generator' not in st.session_state:
    st.session_state.menu_generator = WeeklyMenuGenerator()

# Generate a new weekly menu when the button is clicked
if st.button("Nächste Woche"):
    st.session_state.menu_generator = WeeklyMenuGenerator()

grouped_menu = st.session_state.menu_generator.grouped_menu

# Initialize lists to store meals and their average ratings
meal_names = []
average_ratings = []

# Create list with days of week from Monday to Friday
days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']

# Initialize a counter for unique keys, so multiple ratings for the same meal are possible
rating_counter = 0

# Loop through each day and display the menu of each day to the user
# zip: https://realpython.com/python-zip-function/
for day, meals in zip(days_of_week, grouped_menu): 
    # Unpack the tuple of meals for the day
    veg_meal, non_veg_meal = meals 
    
    st.subheader(day) 

    # Process each meal type (vegetarian and non-vegetarian)
    for meal in [veg_meal, non_veg_meal]:
        # Unpack each meal into ID, name and thumbnail
        meal_id, meal_name, meal_thumb = meal 
        # Initialize rating system for each meal
        rating_system = MealRatingSystem(meal_id=meal_id, meal_name=meal_name)

        st.text(f"{meal_name}")

        # Display the meal image if image exists
        if meal_thumb:
            st.image(meal_thumb)

        # Generate a unique key for each rating and submit button by combining meal ID, day of the week, and the counter
        unique_key = f"{meal_id}_{day}_{rating_counter}"
        rating_counter += 1

        # Capture the users input as a string
        user_input = st.text_input(f"Bewerte {meal_name} von 1 bis 6", key=unique_key)

        # Initialize variables for user rating and whether input is valid
        user_rating = None
        valid_input = True

        # Check if user input is not empty
        if user_input:
            #Try to convert the input to an integer, https://www.w3schools.com/python/python_try_except.asp
            try:
                user_rating = int(user_input)
            except ValueError:
                valid_input = False  #Invalid input, not a number

            # Check if the input is within the valid range
            if valid_input and not (1 <= user_rating <= 6):
                valid_input = False  # Invalid input, out of range

        # Display an error message if the input is invalid and not empty
        if user_input and not valid_input:
            st.error("Bitte geben Sie eine ganzzahlige Bewertung von 1 bis 6 ein.")

        # Display rating button, distinguishable with unique key
        submit_button = st.button(f"Bewertung abgeben für {meal_name}", key=f"btn_{unique_key}")

        # If the button is clicked and the input is valid, process the rating
        if submit_button and valid_input:
            # Add user rating to the list and calculate the new average
            new_average_rating = rating_system.add_user_rating_to_list(user_rating)

            # Update the average rating display in the UI
            st.write(f"Neuer durchschnittlicher Bewertung für {meal_name}: {new_average_rating}")
        
        # Adds the current meal name to a list, used in data frame
        meal_names.append(meal_name)

        # Calculate the average rating, used in data frame
        if rating_system.ratings:
            average_rating = round(sum(rating_system.ratings) / len(rating_system.ratings), 1)
        else:
            average_rating = 0
        average_ratings.append(average_rating)

# Create a data frame with the meal names and average ratings
data = pd.DataFrame({
    'Meal': meal_names,
    'Average Rating': average_ratings
})

# Visualize the average ratings derived from data frame
st.subheader("Durchschnittliche Bewertungen der Gerichte")
st.bar_chart(data.set_index('Meal'))
import streamlit as st
import pandas as pd
from menu_generator import WeeklyMenuGenerator
from rating import MealRatingSystem

# Titel der Anwendung
st.title("Wochenplan")

# Initialisiere den Menügenerator als Session State Variable, um ihn über Neuladungen hinweg zu behalten
if 'menu_generator' not in st.session_state:
    st.session_state.menu_generator = WeeklyMenuGenerator()

# Generiere ein neues wöchentliches Menü, wenn der Button geklickt wird, oder verwende das vorhandene
if st.button("Nächste Woche"):
    st.session_state.menu_generator = WeeklyMenuGenerator()
grouped_menu = st.session_state.menu_generator.grouped_menu

# Zeige das gruppierte wöchentliche Menü von Montag bis Freitag an
days_of_week = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
for day, meals in zip(days_of_week, grouped_menu):
    veg_meal, non_veg_meal = meals
    st.subheader(day)

    # Verarbeite jede Mahlzeitentyp (vegetarisch und nicht-vegetarisch)
    for meal in [veg_meal, non_veg_meal]:
        meal_id, meal_name = meal
        rating_system = MealRatingSystem(meal_id)

        # Zeige den Namen der Mahlzeit an
        st.text(f"{meal_name} (Aktuelle Bewertungen)")

        # Eingabe für neue Bewertungen über Streamlit
        user_rating = st.number_input("Bewerte dieses Gericht von 1 bis 6", min_value=1, max_value=6, step=1,
                                      key=f"{meal_id}_{day}")
        submit_button = st.button(f"Bewertung abgeben für {meal_name}", key=f"btn_{meal_id}_{day}")
        if submit_button and 1 <= user_rating <= 6:
            new_average_rating = rating_system.add_user_rating_to_list(user_rating)
            rating_system.save_ratings(rating_system.ratings)

            # Visualisiere den aktualisierten Durchschnitt als Balkendiagramm direkt unter jedem Gericht
            data = pd.DataFrame({'Durchschnittsbewertung': [new_average_rating]}, index=[meal_name])
            st.bar_chart(data)
        elif submit_button:
            st.error("Bitte bewerte dein Gericht mit einer Zahl von 1 bis 6")



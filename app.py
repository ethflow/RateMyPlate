import streamlit as st
import plotly.graph_objects as go
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

        # Eingabe für neue Bewertungen über Streamlit
        user_rating = st.number_input("Bewerte dieses Gericht von 1 bis 6", min_value=1, max_value=6, step=1,
                                      key=f"{meal_id}_{day}")
        submit_button = st.button(f"Bewertung abgeben für {meal_name}", key=f"btn_{meal_id}_{day}")
        if submit_button and 1 <= user_rating <= 6:
            new_average_rating = rating_system.add_user_rating_to_list(user_rating)
            rating_system.save_ratings(rating_system.ratings)

            # Erstelle ein Plotly-Bar-Diagramm mit dem aktualisierten Durchschnitt
            fig = go.Figure(go.Bar(
                x=[meal_name], y=[new_average_rating],
                text=[f"{new_average_rating}"], textposition='auto',
                marker=dict(color='blue', line=dict(color='rgb(8,48,107)', width=1.5))
            ))
            fig.update_layout(
                title_text='Aktualisierte Durchschnittsbewertung',
                xaxis=dict(title='Gericht'),
                yaxis=dict(title='Durchschnittsbewertung', range=[0, 6]),
                plot_bgcolor='rgba(245, 246, 249, 1)',
                showlegend=False
            )
            fig.update_traces(marker_line_width=0.5, width=0.2)  # Kontrolle über die Balkenbreite
            st.plotly_chart(fig, use_container_width=True)
        elif submit_button:
            st.error("Bitte bewerte dein Gericht mit einer Zahl von 1 bis 6")

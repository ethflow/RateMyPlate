import streamlit as st
import plotly.graph_objects as go
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

    # Process each meal type (vegetarian and non-vegetarian)
    for meal in [veg_meal, non_veg_meal]:
        meal_id, meal_name = meal
        rating_system = MealRatingSystem(meal_id)

        # Display meal name
        st.text(f"{meal_name} (Aktuelle Bewertungen)")

        # Streamlit input for new rating
        user_rating = st.number_input("Bewerte dieses Gericht von 1 bis 6", min_value=1, max_value=6, step=1,
                                      key=f"{meal_id}_{day}")
        submit_button = st.button(f"Bewertung abgeben für {meal_name}", key=f"btn_{meal_id}_{day}")
        if submit_button and 1 <= user_rating <= 6:
            new_average_rating = rating_system.add_user_rating_to_list(user_rating)
            rating_system.save_ratings(rating_system.ratings)

            # Create a Plotly bar chart with the updated average rating
            fig = go.Figure(
                data=[go.Bar(x=[meal_name], y=[new_average_rating], text=[new_average_rating], textposition='auto')])
            fig.update_traces(marker_color='blue', marker_line_width=1.5, width=0.1)  # Make the bar thinner
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
                              xaxis_title="", yaxis_title="Rating",
                              yaxis=dict(showgrid=False, tickvals=[1, 2, 3, 4, 5, 6]))
            st.plotly_chart(fig, use_container_width=True)
        elif submit_button:
            st.error("Bitte bewerte dein Gericht mit einer Zahl von 1 bis 6")

import streamlit as st
import weeklymenugenerator


menu_generator = WeeklyMenuGenerator()
print("Grouped weekly menu (Monday to Friday):")
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
for day, meals in zip(days_of_week, menu_generator.grouped_menu):
    veg_meal, non_veg_meal = meals
    print(f"{day}: Vegetarian meal - {veg_meal[1]}, Non-vegetarian meal - {non_veg_meal[1]}")


st.write("it works, programming god")
st.write(menu_generator)

st.write("Works properly")
st.write("Works for me too")



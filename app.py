import streamlit as st
from feature_01 import return_even

original_list = [i for i in range(10)]

even_list = return_even(original_list)

st.write("it works, programming god")
st.write(even_list)

st.write("Works properly")
st.write("Works for me too")



import streamlit as st
import pandas as pd
#https://streamlit.io/
#streamlit run example.py [ARGUMENTS]
st.write("# Hermit Crabs *yee haw*")
secondInterval = 0
# while secondInterval >= 5 and secondInterval <= 60:
# secondInterval = st.number_input('Insert an interval between 5 and 60')
secondInterval = st.number_input("Insert a time tracking interval in seconds", min_value=5, max_value=60, step=1)
st.write('The current number is ', secondInterval)


video_file = st.file_uploader("Please enter the video to label ")
if video_file is not None:
    print("you did it :D")

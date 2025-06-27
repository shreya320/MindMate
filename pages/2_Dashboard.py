import streamlit as st
from components.mood_dashboard import show_dashboard

st.set_page_config(page_title="📊 Mood Dashboard", layout="centered")

st.title("📊 Mood Dashboard")
st.write("Explore your emotional trends over time based on your journal entries.")

show_dashboard()

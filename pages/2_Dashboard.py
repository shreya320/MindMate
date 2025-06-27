# pages/1_Dashboard.py

import streamlit as st
from components.mood_dashboard import show_dashboard

# Set page title and layout
st.set_page_config(page_title="📊 Mood Dashboard", layout="centered")

# Main content
st.title("📊 Mood Dashboard")
st.write("Explore your emotional trends over time based on your journal entries.")

# Show mood analysis graphs
show_dashboard()

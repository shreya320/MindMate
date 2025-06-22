# app.py

import streamlit as st
from journal_handler import save_entry
from mood_analysis import analyze_sentiment
from response import generate_feedback
from prompt_generator import get_prompt
from mood_dashboard import show_dashboard

st.set_page_config(page_title="MindMate Lite", layout="centered")

st.title("🧠 MindMate Lite")
st.subheader("Your AI-powered emotional journaling assistant")

# -- Journal Input Section --
st.markdown("### ✍️ What's on your mind today?")
user_input = st.text_area("Write your thoughts below:", height=200)

if st.button("Submit Entry"):
    if user_input.strip():
        mood = analyze_sentiment(user_input)
        ai_reply = generate_feedback(user_input, mood)
        save_entry(user_input, mood, ai_reply)
        st.success("Entry saved!")
        st.markdown("### 🤖 AI Response:")
        st.write(ai_reply)
        st.markdown(f"**Detected Mood:** `{mood}`")
    else:
        st.warning("Please write something before submitting.")

# -- Prompt Button --
if st.button("Need a prompt?"):
    st.markdown("### ✨ Journaling Prompt:")
    st.write(get_prompt())

# -- Dashboard --
st.markdown("---")
st.markdown("### 📊 Mood Dashboard")
show_dashboard()

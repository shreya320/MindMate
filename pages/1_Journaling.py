import sys
import pandas as pd
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'components')))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from components.journal_handler import save_entry
from components.mood_analysis import analyze_sentiment
from components.response import generate_feedback
from components.prompt_generator import get_prompt
st.set_page_config(page_title="MindMate Lite", layout="centered")



st.title("🧠 MindMate Lite")
st.subheader("Your AI-powered emotional journaling assistant")


# --- Prompt Button ---

st.markdown("## ✨ Need a journaling prompt?")
if "show_prompt" not in st.session_state:
    st.session_state.show_prompt = False

if st.button("📝 Need a prompt?"):
    st.session_state.show_prompt = True

if st.session_state.show_prompt:
    mood_choice = st.selectbox(
        "Choose your current mood (or leave as Default):",
        ["Default", "joy", "sadness", "anger", "fear", "neutral", "surprise", "disgust"]
    )

    if mood_choice == "Default":
        try:
            df = pd.read_csv("journal_log.csv", names=["Timestamp", "Entry", "Mood", "AI_Response"])
            if not df.empty:
                last_entry = df.iloc[-1]["Entry"]
                detected_mood = analyze_sentiment(last_entry)
                prompt = get_prompt(detected_mood)
             
            else:
                prompt = get_prompt()
                st.warning("No journal entries found. Showing a general prompt.")
        except FileNotFoundError:
            prompt = get_prompt()
            st.warning("Journal log not found. Showing a general prompt.")
    else:
        prompt = get_prompt(mood_choice)

    st.markdown("### 💡 Prompt Suggestion:")
    st.success(f"_{prompt}_")



# -- Journal Input Section --

st.markdown("### ✍️ What's on your mind today?")
user_input = st.text_area("Write your thoughts below:", height=200)

if st.button("Submit Entry"):
    if user_input.strip():
        mood = analyze_sentiment(user_input)
        ai_reply = generate_feedback(user_input, mood)
        save_entry(user_input, mood, ai_reply)
        st.success("Entry saved!")
        st.markdown("### Response:")
        st.write(ai_reply)
        st.markdown(f"**Detected Mood:** `{mood}`")
    else:
        st.warning("Please write something before submitting.")


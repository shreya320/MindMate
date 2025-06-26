import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="MindMate Lite",
    page_icon="🧠",
    layout="centered",
)

# --- Banner or Visual ---
st.image("image.jpeg", height=200)

# --- Title ---
st.markdown("""
<div style="text-align: center;">
    <h1 style="font-size: 3em; margin-bottom: 0.2em;">🧠 MindMate Lite</h1>
    <p style="font-size: 1.2em; color: #555;">Your AI-powered journaling companion for mental wellness</p>
</div>
""", unsafe_allow_html=True)

# --- Divider ---
st.markdown("---")

# --- Features Section ---
st.markdown("""
### 🌟 What You Can Do:
""")
cols = st.columns(2)
with cols[0]:
    st.markdown("- 📝 Journal your thoughts")
    st.markdown("- 💬 Get emotional insights")
    st.markdown("- 📊 Track your mood")

with cols[1]:
    st.markdown("- 🤗 Receive empathetic responses")
    st.markdown("- 🌈 Discover gentle prompts")

# --- CTA ---
st.markdown("---")
st.markdown("### ✨ Ready to begin your journey?")
st.page_link("pages/1_Journaling.py", label="🧠 Start Journaling", icon="📝")


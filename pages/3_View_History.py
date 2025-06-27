import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="📚 Journal History", layout="wide")

# Load data
try:
    df = pd.read_csv("journal_log.csv", names=["Timestamp", "Entry", "Mood", "AI_Response"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
    df = df.dropna(subset=["Timestamp"])
    df = df[::-1].reset_index(drop=True)

    if df.empty:
        st.info("No journal entries found yet.")
    else:
        st.markdown("## 🧾 Your Journal Entries")
        st.markdown("---")

        # --- Filters ---
        with st.expander("🔍 Filter your entries"):
            col1, col2, col3 = st.columns(3)
            with col1:
                date_filter = st.selectbox("By Time", ["All Time", "Past 7 Days", "Past 30 Days"])
            with col2:
                mood_filter = st.selectbox("By Mood", ["All"] + sorted(df["Mood"].unique()))
            with col3:
                sort_order = st.selectbox("Sort", ["Newest First", "Oldest First"])

        # --- Apply Filters ---
        if date_filter == "Past 7 Days":
            df = df[df["Timestamp"] >= datetime.now() - timedelta(days=7)]
        elif date_filter == "Past 30 Days":
            df = df[df["Timestamp"] >= datetime.now() - timedelta(days=30)]
        if mood_filter != "All":
            df = df[df["Mood"] == mood_filter]
        df = df.sort_values("Timestamp", ascending=(sort_order == "Oldest First")).reset_index(drop=True)

        if "open_entry" not in st.session_state:
            st.session_state.open_entry = None

        # --- Display Cards: 3 per row ---
        for i in range(0, len(df), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j >= len(df):
                    continue
                row = df.iloc[i + j]
                idx = i + j
                with cols[j]:
                    with st.container():
                        is_open = st.session_state.open_entry == idx

                        html = f"""
                        <div style="
                            background-color: #f9f9f9;
                            padding: 1rem;
                            border-radius: 10px;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                            color: black;
                            font-family: Arial;
                            margin-bottom: 1rem;
                            min-height: 220px;
                        ">
                            <h4 style="margin-bottom: 0.4rem;">🕒 {row['Timestamp'].strftime('%b %d, %Y – %I:%M %p')}</h4>
                            <p style="font-weight: bold; margin: 0 0 0.5rem 0;">Mood: 
                                <span style="background-color: #e0e0e0; border-radius: 5px; padding: 0.2rem 0.5rem;">
                                    {row['Mood'].capitalize()}
                                </span>
                            </p>
                        """

                        st.markdown(html, unsafe_allow_html=True)

                        if st.button("📖 View Entry" if not is_open else "🔒 Hide Entry", key=f"btn_{idx}"):
                            if is_open:
                                st.session_state.open_entry = None
                            else:
                                st.session_state.open_entry = idx

                        if is_open:
                            details = f"""
                            <div style="
                                background-color: #ffffff;
                                border-top: 1px solid #ccc;
                                margin-top: 0.8rem;
                                padding: 1rem;
                                color: black;
                                border-radius: 8px;
                            ">
                                <p style="margin-bottom: 0.5rem;"><strong>Your Entry:</strong></p>
                                <p style="line-height: 1.8; margin-bottom: 1rem;">{row['Entry']}</p>
                                <p style="margin-bottom: 0.5rem;"><strong>AI Response:</strong></p>
                                <p style="line-height: 1.8; background-color: #eef; padding: 0.8rem; border-radius: 6px;">{row['AI_Response']}</p>
                            </div>
                            """
                            st.markdown(details, unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

except FileNotFoundError:
    st.warning("Journal file not found. Submit some entries first.")

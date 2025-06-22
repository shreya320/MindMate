# mood_dashboard.py

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def show_dashboard(csv_file="journal_log.csv"):
    try:
        df = pd.read_csv(csv_file, names=["Timestamp", "Entry", "Mood", "AI_Response"])
        if df.empty:
            st.info("No data yet. Submit some journals to see your dashboard.")
            return
        
        # Pie chart
        mood_counts = df["Mood"].value_counts()
        st.markdown("#### 🥧 Mood Distribution")
        fig1, ax1 = plt.subplots()
        ax1.pie(mood_counts, labels=mood_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

        # Mood trend over time
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        daily_moods = df.groupby(df["Timestamp"].dt.date)["Mood"].apply(lambda x: x.value_counts().idxmax())
        st.markdown("#### 📈 Mood Trend Over Time")
        fig2, ax2 = plt.subplots()
        daily_moods.value_counts().sort_index().plot(kind='bar', ax=ax2)
        st.pyplot(fig2)

    except FileNotFoundError:
        st.warning("Journal log not found. Add some entries first.")

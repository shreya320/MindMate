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


        # Convert mood to score
        mood_scores = {"POSITIVE": 1, "NEUTRAL": 0, "NEGATIVE": -1}
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df["Mood_Score"] = df["Mood"].map(mood_scores)

        # Average mood score per day
        daily_trend = df.groupby(df["Timestamp"].dt.date)["Mood_Score"].mean()

        # Plotting the trendline
        st.markdown("#### 📈 Mood Trend Over Time")
        fig, ax = plt.subplots()
        daily_trend.plot(kind='line', marker='o', ax=ax)
        ax.set_ylabel("Mood Score")
        ax.set_xlabel("Date")
        ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
        st.pyplot(fig)

    except FileNotFoundError:
        st.warning("Journal log not found. Add some entries first.")

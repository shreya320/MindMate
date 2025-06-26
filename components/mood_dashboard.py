# components/mood_dashboard.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np

def show_dashboard(csv_file="journal_log.csv"):
    try:
        df = pd.read_csv(csv_file, names=["Timestamp", "Entry", "Mood", "AI_Response"])
        if df.empty:
            st.info("No data yet. Submit some journals to see your dashboard.")
            return

        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df["Date"] = df["Timestamp"].dt.date

        # --- Bubble Chart ---
        st.markdown("### 🫧 Emotion Bubble Chart")

        mood_counts = df["Mood"].value_counts().reset_index()
        mood_counts.columns = ["Mood", "Count"]

        mood_colors = {
            "joy": "#4CAF50", "sadness": "#2196F3", "anger": "#F44336",
            "fear": "#9C27B0", "surprise": "#FF9800", "neutral": "#9E9E9E",
            "disgust": "#795548"
        }

        mood_counts["Color"] = mood_counts["Mood"].map(mood_colors).fillna("#607D8B")
        mood_counts["x"] = np.random.rand(len(mood_counts))
        mood_counts["y"] = np.random.rand(len(mood_counts))

        bubble_fig = px.scatter(
            mood_counts,
            x="x",
            y="y",
            size="Count",
            color="Mood",
            color_discrete_map=mood_colors,
            hover_name="Mood",
            size_max=100,
        )

        bubble_fig.update_layout(
            title="Most Frequent Emotions",
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False
        )

        st.plotly_chart(bubble_fig, use_container_width=True)

        # --- Interactive Mood Trend Line Chart ---
        st.markdown("### 📈 Mood Trend Over Time")

        mood_scores = {
            "joy": 2, "surprise": 1, "neutral": 0,
            "sadness": -1, "fear": -1, "anger": -2, "disgust": -2
        }
        df["Mood_Score"] = df["Mood"].map(mood_scores).fillna(0)
        daily_avg = df.groupby("Date")["Mood_Score"].mean().reset_index()

        trend_fig = go.Figure()
        trend_fig.add_trace(go.Scatter(
            x=daily_avg["Date"],
            y=daily_avg["Mood_Score"],
            mode="lines+markers",
            line=dict(color="royalblue", width=2),
            marker=dict(size=8),
            hovertemplate='Date: %{x}<br>Mood Score: %{y}<extra></extra>'
        ))

        trend_fig.update_layout(
            title="Average Mood Score by Day",
            xaxis_title="Date",
            yaxis_title="Mood Score",
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(range=[-2.5, 2.5])
        )

        st.plotly_chart(trend_fig, use_container_width=True)

    except FileNotFoundError:
        st.warning("Journal log not found. Add some entries first.")

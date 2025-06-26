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

        # --- Shared Styling ---
        mood_colors = {
            "joy": "#FFD700",       # bright gold
            "sadness": "#1E88E5",   # strong blue
            "anger": "#E53935",     # bright red
            "fear": "#8E24AA",      # purple
            "surprise": "#FB8C00",  # orange
            "neutral": "#757575",   # gray
            "disgust": "#6D4C41"    # brown
        }

        font_style = dict(family="Arial", size=16, color="#212121")
        plot_bg = "#FAFAFA"
        hover_bg = "#FFFFFF"

        # --- Bubble Chart ---
        st.markdown("### 🫧 Emotion Bubble Chart")

        mood_counts = df["Mood"].value_counts().reset_index()
        mood_counts.columns = ["Mood", "Count"]
        mood_counts["Color"] = mood_counts["Mood"].map(mood_colors).fillna("#607D8B")
        np.random.seed(42)
        mood_counts["x"] = np.random.rand(len(mood_counts)) * 100
        mood_counts["y"] = np.random.rand(len(mood_counts)) * 100

        bubble_fig = px.scatter(
            mood_counts,
            x="x",
            y="y",
            size="Count",
            color="Mood",
            color_discrete_map=mood_colors,
            hover_name="Mood",
            hover_data={"Count": True, "x": False, "y": False},
            size_max=100,
        )

        bubble_fig.update_layout(
            title="Most Frequent Emotions",
            title_font=dict(size=24, family="Arial", color="#212121"),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            plot_bgcolor=plot_bg,
            paper_bgcolor=plot_bg,
            showlegend=False,
            font=font_style,
            hoverlabel=dict(
                bgcolor=hover_bg,
                font_size=12,
                font_family="Calibri",
                font_color="#000000"
            ),
            height=450
        )

        st.plotly_chart(bubble_fig, use_container_width=True)

               # --- Trend Line Chart by Entry Index ---
        st.markdown("### 📈 Mood Trend by Entry")

        mood_scores = {
            "happiness": 2, "joy": 2, "surprise": 1, "neutral": 0,
            "sadness": -1, "fear": -1, "anger": -2, "disgust": -2
        }

        df["Mood_Score"] = df["Mood"].map(mood_scores).fillna(0)
        df_sorted = df.sort_values("Timestamp").reset_index(drop=True)
        df_sorted["Entry_No"] = df_sorted.index + 1  # Start from 1

        trend_colors = df_sorted["Mood"].map(mood_colors).fillna("#607D8B")

        trend_fig = go.Figure()
        trend_fig.add_trace(go.Scatter(
            x=df_sorted["Entry_No"],
            y=df_sorted["Mood_Score"],
            mode="lines+markers",
            line=dict(color="rgba(33, 150, 243, 0.5)", width=3, shape='spline'),
            marker=dict(
                size=10,
                color=trend_colors,
                line=dict(width=1.5, color='white')
            ),
            text=df_sorted["Entry"],
            customdata=df_sorted[["Mood", "Timestamp"]],
            hovertemplate=(
                "<b>Mood</b>: %{customdata[0]}<br>"
                "<b>Time</b>: %{customdata[1]|%b %d, %Y %I:%M %p}<br>"
                "<b>Score</b>: %{y}<br>"
            )
        ))

        trend_fig.update_layout(
            title="Mood Score Over Journal Entries",
            xaxis_title="Entry Number",
            yaxis_title="Mood Score",
            plot_bgcolor=plot_bg,
            paper_bgcolor=plot_bg,
            font=font_style,
            xaxis=dict(
                title_font=dict(color="black"),
                tickfont=dict(color="black")
            ),
            yaxis=dict(
                title_font=dict(color="black"),
                tickfont=dict(color="black"),
                range=[-2.5, 2.5],
                showgrid=True,
                zeroline=True,
                zerolinecolor='black'
            ),
            hoverlabel=dict(
                bgcolor=hover_bg,
                font_size=12,
                font_family="Calibri",
                font_color="#000000"
            ),
            margin=dict(t=60, l=40, r=40, b=40),
            height=500
        )

        st.plotly_chart(trend_fig, use_container_width=True)



                # --- Stacked Bar Chart: Emotion Breakdown Across All Days ---
        st.markdown("### 📊 Daily Emotion Distribution")

        # Prepare data: count of each mood per day
        mood_daily_counts = df.groupby(["Date", "Mood"]).size().reset_index(name="Count")

        # Pivot to get moods as columns
        pivot_df = mood_daily_counts.pivot(index="Date", columns="Mood", values="Count").fillna(0)
        pivot_df = pivot_df.sort_index()  # Ensure dates are sorted

        # Build stacked bar chart
        bar_fig = go.Figure()
        for mood in pivot_df.columns:
            bar_fig.add_trace(go.Bar(
                name=mood,
                x=pivot_df.index.astype(str),
                y=pivot_df[mood],
                marker_color=mood_colors.get(mood, "#607D8B"),
                hovertemplate='<b>Date:</b> %{x}<br><b>Mood:</b> ' + mood + '<br><b>Count:</b> %{y}<extra></extra>'
            ))

        bar_fig.update_layout(
            barmode="stack",
            title="Daily Emotion Distribution (Stacked)",
            xaxis_title="Date",
            yaxis_title="Count",
            plot_bgcolor=plot_bg,
            paper_bgcolor=plot_bg,
            font=font_style,
            xaxis=dict(tickangle=45, tickfont=dict(color="black"), title_font=dict(color="black")),
            yaxis=dict(gridcolor="#E0E0E0", tickfont=dict(color="black"), title_font=dict(color="black")),
            hoverlabel=dict(
                bgcolor=hover_bg,
                font_size=12,
                font_family="Calibri",
                font_color="#000000"
            ),
            legend=dict(title="Moods",font_color="Black"),
            height=500
        )

        st.plotly_chart(bar_fig, use_container_width=True)



    except FileNotFoundError:
        st.warning("Journal log not found. Add some entries first.")

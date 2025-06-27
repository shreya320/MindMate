import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from collections import Counter
import re

st.set_page_config(page_title="🔍 Mood Insights", layout="wide")

try:
    df = pd.read_csv("journal_log.csv", names=["Timestamp", "Entry", "Mood", "AI_Response"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
    df = df.dropna(subset=["Timestamp"])
    df = df.sort_values("Timestamp")

    if df.empty:
        st.info("No journal entries yet. Come back once you’ve submitted a few.")
    else:
        st.title("🔍 Mood Insights")

        # Time range selector
        date_range = st.selectbox("Select time range", ["Past 7 Days", "Past 30 Days", "All Time"])
        if date_range == "Past 7 Days":
            filtered_df = df[df["Timestamp"] >= datetime.now() - timedelta(days=7)]
        elif date_range == "Past 30 Days":
            filtered_df = df[df["Timestamp"] >= datetime.now() - timedelta(days=30)]
        else:
            filtered_df = df

        tab1, tab2, tab3 = st.tabs(["📈 Mood Forecast", "☁️ Word Cloud", "📊 Dominant Emotion Trend"])


        # Tab 1:
        with tab1:
            st.subheader("📈 Predicted Mood for Tomorrow")

            df["Mood_Score"] = df["Mood"].map({"joy":2, "surprise":1, "neutral":0, "sadness":-1, "fear":-1, "anger":-2, "disgust":-2}).fillna(0)

            if len(df) >= 3:
                forecast = round(df["Mood_Score"].rolling(3).mean().iloc[-1])
                score_to_mood = {2:"Joy", 1:"Surprise", 0:"Neutral", -1:"Sadness", -2:"Anger"}
                predicted_mood = score_to_mood.get(forecast, "Neutral")
                st.success(f"Based on recent trends, you might feel **{predicted_mood}** tomorrow.")

                st.markdown("#### Mood Score Trend")
                df_sorted = df.sort_values("Timestamp").reset_index(drop=True)
                df_sorted["Entry_No"] = df_sorted.index + 1

                trend_fig = go.Figure()
                trend_fig.add_trace(go.Scatter(
                    x=df_sorted["Entry_No"],
                    y=df_sorted["Mood_Score"],
                    mode="lines+markers",
                    line=dict(color="#1E88E5", width=2),
                    marker=dict(size=8),
                    hovertext=df_sorted["Mood"],
                    name="Mood Score"
                ))

                trend_fig.update_layout(
                    xaxis_title="Entry Number",
                    yaxis_title="Mood Score",
                    height=400,
                    margin=dict(t=30, b=20),
                    plot_bgcolor="#FAFAFA",
                    paper_bgcolor="#FAFAFA"
                )

                st.plotly_chart(trend_fig, use_container_width=True)

                if forecast < 0:
                    st.markdown("---")
                    st.info("**Feeling low? Here’s something to uplift you:**")
                    st.video("https://www.youtube.com/watch?v=GXy__kBVq1M")
                    st.caption("\"Every storm runs out of rain.\" – Maya Angelou")
            else:
                st.warning("Not enough data to forecast mood. Add a few more entries!")

            st.divider()
            st.subheader("⚠️ Flagged Entries Check")
            risk_keywords = ["end it all", "hopeless", "no point", "give up", "can't go on", "worthless"]
            risk_found = df["Entry"].str.contains('|'.join(risk_keywords), case=False, na=False)
            risky_entries = df[risk_found]

            if not risky_entries.empty:
                st.error("Some entries may contain signs of distress. Please take care. 💛")
                st.markdown("**Resources:**")
                st.markdown("- [iCall India Mental Health Helpline](https://icallhelpline.org/)")
                st.markdown("- [AASRA India (24x7): +91-9820466726](https://www.aasra.info/)")

                st.markdown("### 📌 Flagged Entries")
                for _, row in risky_entries.iterrows():
                    st.markdown(f"- *{row['Timestamp'].strftime('%b %d, %Y')}*: \"{row['Entry']}\"")
            else:
                st.success("No high-risk phrases detected.")

        # --- Word Cloud Tab ---
        with tab2:
            st.subheader("☁️ Common Words from the Past Week")
            past_week = df[df["Timestamp"] >= datetime.now() - timedelta(days=7)]

            if not past_week.empty:
                all_text = " ".join(past_week["Entry"].astype(str))

                wc = WordCloud(width=1000, height=500, background_color="white", colormap='viridis',
                               max_words=50, random_state=42).generate(all_text)

                with st.container():
                    st.markdown("""
                    <div style='background-color: #f4f4f4; padding: 1rem; border-radius: 10px;'>
                        <p style='font-size: 1rem; color: #333;'>This cloud represents the most frequent words you've used in your journal over the past week. Larger words appeared more often.</p>
                    </div>
                    """, unsafe_allow_html=True)

                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)

                    words = re.findall(r'\b\w{4,}\b', all_text.lower())
                    word_freq = Counter(words).most_common(10)

                    st.markdown("### 🔠 Top 10 Frequent Words:")
                    for word, freq in word_freq:
                        st.markdown(f"- **{word}** ({freq} times)")
            else:
                st.info("No entries in the last 7 days.")

        # --- Dominant Emotion Tab ---
        with tab3:
            st.subheader("📊 Dominant Emotion Over the Past Week")
            past_week_df = df[df["Timestamp"] >= datetime.now() - timedelta(days=7)]
            if not past_week_df.empty:
                dominant = past_week_df["Mood"].value_counts().idxmax()
                st.info(f"Your most frequent emotion this week was **{dominant}**.")

                mood_daily = past_week_df.groupby([past_week_df["Timestamp"].dt.date, "Mood"]).size().reset_index(name="Count")

                fig = go.Figure()
                for mood in mood_daily["Mood"].unique():
                    subset = mood_daily[mood_daily["Mood"] == mood]
                    fig.add_trace(go.Bar(
                        x=subset["Timestamp"].astype(str),
                        y=subset["Count"],
                        name=mood
                    ))
                fig.update_layout(
                    barmode="stack",
                    xaxis_title="Date",
                    yaxis_title="Count",
                    title="Daily Emotion Breakdown (Past Week)",
                    height=400,
                    plot_bgcolor="#fafafa",
                    paper_bgcolor="#000000"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No entries available from the past week.")

except FileNotFoundError:
    st.warning("Journal file not found. Submit some entries first.")

# 🌙 MindMate: A Smart Journaling and Mood Insight App

MindMate is a personal journaling and mood analysis app that helps users reflect on their thoughts, track emotional trends, and receive mental health insights, all in a calming, interactive interface.

---

## 🧠 Features

### ✅ Core Journaling & Reflection

- **Flashcard-style Journal Viewer:** Easily browse through past entries with a flip-card UI.
- **Mood Logging:** Record journal entries alongside mood selections.
- **Mood-Based Resources:** Automatically recommends TED talks, quotes, or calming media when your mood score indicates distress.

### 📊 Insights & Analytics

- **Mood Forecasting:** Predicts your emotional state for tomorrow using recent mood trends.
- **Emotion Trendline:** Visualizes your mood scores over time.
- **Daily Emotion Breakdown:** Stacked bar chart showing dominant emotions per day.
- **Word Cloud Summary:** Extracts commonly used words from your journals.
- **Dominant Weekly Emotion:** Highlights your most frequent emotional state.

### ⚠️ Ethical Care & Safety

- **Risk Phrase Detection:** Automatically detects potentially harmful or distressing language.
- **Emergency Helpline Access:** Shows helplines and support links when risky phrases are found.

---


## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/shreya320gupta/mindmate.git
   cd mindmate
````

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

> Make sure you’ve created a file named `journal_log.csv` in the root folder. The app will generate it as you start journaling.

---

## 📁 Project Structure

```
📂 MindMate/
├── app.py
├── pages/
│   ├── 1_Journalling.py
│   ├── 2_Dashboard.py
|   |── 3_View_History.py
│   |── 4_Mood_Insights.py
|   └── 5_Contact_Me.py
├── journal_log.csv
├── components/
├── requirements.txt
└── README.md
```

---

## 📌 Tech Stack

* **Frontend/UI:** [Streamlit](https://streamlit.io)
* **Visualization:** Plotly, Matplotlib, WordCloud
* **Backend:** Python (Pandas, NumPy, Regex)
* **Other Tools:** Markdown, HTML, CSS (Streamlit-compatible)

---

## 🧠 Future Improvements

* Login & authentication
* Conversational Chatbot replies
* Dark mode support
* Mobile responsiveness


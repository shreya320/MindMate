MINDMATE LITE:
Let users journal their thoughts, get AI-generated comfort messages, track mood trends, and get journaling prompts

things to focus on: 

    make a basic frontend

    users can input their journals (mutliple times?)

    they can ask for a prompt
    - can be refined to be based on moods

    creates a mood dashboard
    - piechart of moods
    - mood trend over a month
    - if mood is below a certain point, offers resources


    if user wants they can get feedback on their journal
    - detects mood (model can classify emotions)
    - gives a response
    - offers encouragement
    - gives emotion aware coaching

    conversational bot 
    - maintain history

    tackle ethics concerns

    predict moods (mood forcasting)
    mental state timeline
    - how you felt over the part week
    - most common words used in the past week




    app.py                  ← main Streamlit app
├── journal_handler.py      ← handles entry saving, retrieval
├── mood_analysis.py        ← sentiment/emotion detection
├── genai_response.py       ← GPT or watsonx AI comfort replies
├── prompt_generator.py     ← journaling prompt logic
├── mood_dashboard.py       ← pie chart + trend chart functions
├── journal_log.csv         ← journal entries get stored here
├── requirements.txt        ← Python libraries
└── README.md               ← for IBM submission
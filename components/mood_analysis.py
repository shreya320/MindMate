# mood_analysis.py

from transformers import pipeline

# Load once
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return result['label']  # 'POSITIVE', 'NEGATIVE', etc.

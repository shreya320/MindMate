from transformers import pipeline

emotion_classifier = pipeline("text-classification", 
                               model="j-hartmann/emotion-english-distilroberta-base", 
                               return_all_scores=True)

def analyze_sentiment(text):
    results = emotion_classifier(text)[0]
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    top_emotion = sorted_results[0]["label"]
    return top_emotion

import csv
from datetime import datetime

def save_entry(text, mood, ai_response, file_path="journal_log.csv"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([now, text, mood, ai_response])

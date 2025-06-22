import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": f"Bearer {API_KEY}"}

def generate_feedback(journal_text, mood):
    prompt = (
        f"You are a kind and supportive assistant.\n"
        f"A person wrote this journal entry:\n"
        f"\"{journal_text}\"\n"
        f"Their mood is {mood.lower()}.\n"
        f"Write a short, emotionally supportive message in response."
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 80,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise error if status code is not 200
        result = response.json()

        print("📦 Raw result:", result)  # <–– ADD THIS for debug

        if isinstance(result, list):
            return result[0]["generated_text"].split(prompt)[-1].strip()
        else:
            print("⚠️ Unexpected format:", result)
            return "Hmm... the AI couldn't respond right now. Try again later?"

    except requests.exceptions.HTTPError as e:
        print("❌ HTTP error:", e)
        print("🔢 Response code:", response.status_code)
        print("📄 Response text:", response.text)
        return "Something went wrong with the AI response. Please try again later."

    except Exception as e:
        print("🔥 General error:", e)
        return "An error occurred. Please try again."

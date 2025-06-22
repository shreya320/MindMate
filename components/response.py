import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def generate_feedback(journal_text, mood):
    print("📝 Journal text:", journal_text)
    print("🎭 Mood:", mood)

    prompt = (
    f"You are a kind, supportive assistant. Respond to this journal entry in a tone that matches the user's mood. "
    f"The user is feeling {mood.lower()} and wrote: '{journal_text}'"
    )


    try:
        print("💬 Sending prompt to Gemini...")
        chat = model.start_chat()
        response = chat.send_message(prompt)
        print("✅ Gemini response received.")

        return response.text.strip()

    except Exception as e:
        print("🔥 Error:", e)
        return "Something went wrong while generating feedback."

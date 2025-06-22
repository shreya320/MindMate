import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

chat = model.start_chat()  # ✅ Start a chat session

response = chat.send_message("I feel anxious and need support. Please help.")
print("Response:", response.text)

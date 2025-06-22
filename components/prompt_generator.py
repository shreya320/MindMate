# prompt_generator.py

import random

prompts = [
    "What’s something you're grateful for today?",
    "Describe a moment that made you smile this week.",
    "Write about something that challenged you recently.",
    "What’s a goal you’re working toward?",
    "What does self-care look like for you today?"
]

def get_prompt():
    return random.choice(prompts)

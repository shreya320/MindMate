import random

mood_prompts = {
    "joy": [
        "What’s bringing you joy today?",
        "Describe a happy moment you want to remember.",
        "What made you laugh recently?"
    ],
    "sadness": [
        "What’s been weighing on your heart lately?",
        "Write about something that made you feel low.",
        "What would you tell a friend feeling this way?"
    ],
    "anger": [
        "What's been frustrating you recently?",
        "Describe a moment where you felt misunderstood.",
        "How do you usually cope when you're angry?"
    ],
    "fear": [
        "What’s making you anxious right now?",
        "Write about a fear and where it might come from.",
        "What would help you feel safer?"
    ],
    "neutral": [
        "Describe your day in 5 words.",
        "What’s something ordinary that you appreciate?",
        "Write whatever comes to mind—no filter."
    ],
    "surprise": [
        "Did something unexpected happen recently?",
        "What’s a good surprise you’ve had?",
        "How do you feel about surprises?"
    ],
    "disgust": [
        "What’s been bothering you lately?",
        "Is there a situation you want to let go of?",
        "Write about something you wish were different."
    ],
    "default": [
        "What’s something you're grateful for today?",
        "Describe a moment that made you smile this week.",
        "Write about something that challenged you recently.",
        "What’s a goal you’re working toward?",
        "What does self-care look like for you today?"
    ]
}

def get_prompt(mood="default"):
    return random.choice(mood_prompts.get(mood, mood_prompts["default"]))

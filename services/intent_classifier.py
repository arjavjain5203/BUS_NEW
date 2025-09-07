import re

# Simple keyword-based classifier
def classify_intent(user_input: str) -> str:
    text = user_input.lower()

    # Greetings / casual
    if any(word in text for word in ["hi", "hello", "hey", "good morning", "good evening"]):
        return "smalltalk"

    # Cancellation policy
    if "cancel" in text or "refund" in text or "policy" in text:
        return "smalltalk"

    # Who are you
    if "who are you" in text or "what are you" in text:
        return "smalltalk"

    # Default to DB queries
    return "database"

def handle_smalltalk(user_input: str) -> str | None:
    """Return a response if it's smalltalk, else None."""
    text = user_input.lower().strip()

    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    wellbeing = ["how are you", "hows it going", "how’s it going", "whats up"]
    faqs = {
        "who are you": "I’m the 🚌 Punjab Bus Assistant, here to help with routes, buses, and more!",
        "cancellation policy": "🚏 Tickets can be cancelled up to 2 hours before departure for a partial refund.",
        "help": "You can ask me about bus availability, routes, timings, or general queries."
    }

    # Greeting
    if any(word in text for word in greetings):
        return "👋 Hello! How can I assist you with buses today?"

    # Well-being
    if any(word in text for word in wellbeing):
        return "😊 I’m just a bot, but I’m doing great! How can I help you?"

    # FAQs
    for key, reply in faqs.items():
        if key in text:
            return reply

    return None  # Not smalltalk

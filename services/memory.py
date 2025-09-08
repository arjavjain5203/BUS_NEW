user_memory = {}

def get_chat_context(user_id: str) -> str:
    """Return the chat history for a given user as a formatted string."""
    history = user_memory.get(user_id, {}).get("history", [])
    return "\n".join(history[-10:])  # last 10 messages

def add_to_context(user_id: str, message: str):
    """Append a new message to user's history."""
    if user_id not in user_memory:
        user_memory[user_id] = {"history": []}
    user_memory[user_id]["history"].append(message)

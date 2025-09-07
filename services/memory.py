from collections import deque

chat_history = deque(maxlen=5)

def get_chat_context():
    return "\n".join([f"User: {u}\nBot: {b}" for u, b in chat_history])

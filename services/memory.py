# Very simple in-memory store (can replace with Redis later)
user_memory = {}

def set_context(user_id: str, key: str, value: str):
    if user_id not in user_memory:
        user_memory[user_id] = {}
    user_memory[user_id][key] = value

def get_context(user_id: str, key: str):
    return user_memory.get(user_id, {}).get(key)

def clear_context(user_id: str):
    if user_id in user_memory:
        user_memory[user_id] = {}

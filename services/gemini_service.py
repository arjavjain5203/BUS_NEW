from google.generativeai import configure, GenerativeModel
from config import API_KEY
from utils.prompts import SCHEMA_PROMPT
from .memory import get_chat_context

configure(api_key=API_KEY)
model = GenerativeModel("gemini-1.5-flash")

def generate_sql(user_input: str) -> str:
    context = get_chat_context()
    response = model.generate_content(
        f"{SCHEMA_PROMPT}\nConversation so far:\n{context}\n\nUser: {user_input}\nSQL:"
    )
    return response.text.strip().strip("```sql").strip("```")

def format_response(raw_results: list, user_input: str) -> str:
    context = get_chat_context()
    response = model.generate_content(
        f"Conversation so far:\n{context}\n\nUser just asked: {user_input}\nHere are SQL query results:\n{raw_results}\n"
        f"Format this as a clear SMS/WhatsApp style reply:"
    )
    return response.text.strip()

def suggest_correction(user_input: str) -> str:
    response = model.generate_content(
        f"You are a spelling assistant for city and stop names in Punjab bus queries.\n"
        f"If the user typed a misspelled city/stop, suggest the corrected version.\n"
        f"If it looks fine, just repeat the input.\n\n"
        f"User input: {user_input}\nCorrected:"
    )
    return response.text.strip()

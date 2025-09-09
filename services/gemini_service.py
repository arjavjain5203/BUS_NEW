import google.generativeai as genai
import json
from google.generativeai import configure, GenerativeModel
from config import API_KEY
from utils.prompts import SCHEMA_PROMPT
from .memory import get_chat_context

configure(api_key=API_KEY)
model = GenerativeModel("gemini-1.5-flash")

def generate_sql(user_input: str, user_id: int) -> str:
    context = get_chat_context(user_id)
    response = model.generate_content(
        f"{SCHEMA_PROMPT}\nConversation so far:\n{context}\n\nUser: {user_input}\nSQL:"
    )
    return response.text.strip().strip("```sql").strip("```")

def format_response(raw_results: list, user_input: str, user_id: int) -> str:
    context = get_chat_context(user_id)
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


    """
    Uses Gemini to classify intent and optionally generate a response.
    """
def detect_intent_and_reply(user_input: str):
    prompt = f"""
    You are an AI assistant for a bus booking/helpdesk system.
    Strictly output only a valid JSON object with exactly these fields:
    - "intent": one of ["bus_query", "casual", "faq", "other"]
    - "response": a natural language reply.

    Example:
    Input: Hi
    Output: {{"intent": "casual", "response": "Hello! How can I assist you with buses today?"}}

    User input: "{user_input}"
    """

    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    print("DEBUG GEMINI RAW:", raw_text)  # 👈 add this

    import re, json
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {"intent": "other", "response": "I'm not sure how to respond."}
    else:
        return {"intent": "other", "response": "I'm not sure how to respond."}

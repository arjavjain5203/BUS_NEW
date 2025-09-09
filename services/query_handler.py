from services.gemini_service import detect_intent_and_reply, generate_sql, format_response, suggest_correction
from database import cursor, db

def handle_user_query(user_input: str, user_id: int = 1):
    parsed = detect_intent_and_reply(user_input)
    intent = parsed["intent"]
    ai_reply = parsed["response"]

    if intent == "bus_query":
        # Apply correction + SQL flow
        corrected_input = suggest_correction(user_input)
        sql_query = generate_sql(corrected_input, user_id=user_id)
        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            response_text = format_response(results, user_input, user_id=user_id)
        except Exception as e:
            response_text = f"⚠️ Sorry, I had trouble fetching bus info: {str(e)}"
    else:
        # For casual/faq/other → use Gemini’s AI reply directly
        response_text = ai_reply

    # Save logs
    cursor.execute(
        """INSERT INTO chatlogs (user_id, message_text, response_text, created_at, intent)
           VALUES (%s, %s, %s, NOW(), %s)""",
        (user_id, user_input, response_text, intent)
    )
    db.commit()

    return response_text

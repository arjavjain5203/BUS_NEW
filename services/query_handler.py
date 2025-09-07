import datetime
from services.gemini_service import generate_sql, format_response, suggest_correction
from services.intent_classifier import classify_intent
from services.smalltalk_service import handle_smalltalk
from database import cursor, db

def handle_user_query(user_input: str, user_id: int = 1) -> str:
    """Process the user input and return the response text."""

    correction_applied = None  # Track if we corrected user query

    # 🔹 Step 1: Intent detection
    intent = classify_intent(user_input)

    if intent == "smalltalk":
        response_text = handle_smalltalk(user_input)

    else:
        # 🔹 Step 2: Try SQL query
        sql_query = generate_sql(user_input)
        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()
        except Exception as e:
            results = {"error": str(e)}

        # 🔹 Step 3: Fallback with typo correction
        if "error" in results or not results:
            correction = suggest_correction(user_input)
            if correction and correction.lower() != user_input.lower():
                correction_applied = correction
                corrected_sql = generate_sql(correction)
                try:
                    cursor.execute(corrected_sql)
                    results = cursor.fetchall()
                except Exception as e:
                    results = {"error": str(e)}

                if results and "error" not in results:
                    response_text = format_response(results, correction)
                    response_text = f"🤖 I noticed a typo. Showing results for *{correction}* instead of *{user_input}*.\n\n{response_text}"
                else:
                    response_text = f"❌ Couldn’t find results for *{user_input}*. Try checking the spelling."
            else:
                response_text = f"❌ Couldn’t find results for *{user_input}*. Please try again."
        else:
            response_text = format_response(results, user_input)

    # 🔹 Step 4: Save logs
    cursor.execute(
        """INSERT INTO chatlogs (user_id, message_text, response_text, created_at, correction_applied)
           VALUES (%s, %s, %s, %s, %s)""",
        (user_id, user_input, response_text, datetime.datetime.now(), correction_applied)
    )
    db.commit()

    return response_text

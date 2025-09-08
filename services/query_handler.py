import re
from services.gemini_service import generate_sql, format_response, suggest_correction
from database import cursor, db

def handle_user_query(user_input: str, user_id: int = 1):
    text = user_input.lower().strip()

    # Step 1: detect "from X to Y"
    match = re.search(r"from\s+([\w\s]+)\s+to\s+([\w\s]+)", text)
    if match:
        origin = match.group(1).strip()
        destination = match.group(2).strip()

        # Apply typo correction for both cities
        origin = suggest_correction(origin)
        destination = suggest_correction(destination)

        sql_query = f"""
            SELECT * FROM buses
            WHERE origin LIKE '%{origin}%' AND destination LIKE '%{destination}%'
        """
    else:
        # fallback: normal query through Gemini
        corrected_input = suggest_correction(user_input)
        sql_query = generate_sql(corrected_input)

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
    except Exception as e:
        results = {"error": str(e)}

    response_text = format_response(results, user_input)

    cursor.execute(
        """INSERT INTO chatlogs (user_id, message_text, response_text, created_at)
           VALUES (%s, %s, %s, NOW())""",
        (user_id, user_input, response_text)
    )
    db.commit()

    return response_text

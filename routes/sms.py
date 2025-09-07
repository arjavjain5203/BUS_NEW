from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from services.query_handler import handle_user_query

router = APIRouter()

@router.post("/sms")
async def sms_webhook(Body: str = Form(...), From: str = Form(...)):
    response_text = handle_user_query(Body, user_id=2)

    beautified = (
        f"🚌 Punjab Bus Assistant\n\n"
        f"{response_text}\n\n"
        f"🚏 Reply anytime for more help!"
    )
    return PlainTextResponse(content=beautified)

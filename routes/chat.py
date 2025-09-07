# from fastapi import APIRouter, Form
# from fastapi.responses import JSONResponse
# from services.query_handler import handle_user_query

# router = APIRouter()

# @router.post("/chat")
# async def chat_webhook(message: str = Form(...)):
#     response_text = handle_user_query(message, user_id=3)
#     return JSONResponse({"reply": response_text})
#############

# chat.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.query_handler import handle_user_query
from models.chat_request import ChatRequest # ✅ Import the Pydantic model

router = APIRouter()

@router.post("/chat")
async def chat_webhook(request: ChatRequest): # ✅ Accept the Pydantic model
    response_text = handle_user_query(request.message, user_id=request.user_id)
    return JSONResponse({"reply": response_text})
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: int = 1
    message: str

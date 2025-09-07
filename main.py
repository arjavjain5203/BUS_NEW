from fastapi import FastAPI
from routes import sms, whatsapp, chat

app = FastAPI(title="Punjab Bus Assistant API")

app.include_router(sms.router)
app.include_router(whatsapp.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Punjab Bus Assistant API is running 🚍"}

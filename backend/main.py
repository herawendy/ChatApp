from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {
        "message": "Backend is running!"
    }

@app.post("/api/message")
def receive_message(data: MessageRequest):
    message = data.message.lower()

    if "hello" in message:
        reply = "Hello! 很高興認識你！"
    elif "python" in message:
        reply = "Python 很適合拿來做 Backend。"
    elif "render" in message:
        reply = "Render 可以部署我們的 FastAPI Backend。"
    else:
        reply = f"後端收到你的訊息：{data.message}"

    return {
        "success": True,
        "reply": reply
    }

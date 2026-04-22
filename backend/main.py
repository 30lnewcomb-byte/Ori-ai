from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Ori Backend")

# Request format
class ChatRequest(BaseModel):
    message: str

# Simple chat endpoint (Phase 1 brain = placeholder)
@app.post("/chat")
def chat(req: ChatRequest):
    user_message = req.message.lower()

    # super simple responses for now
    if "hello" in user_message:
        response = "Hey 👋 I'm Ori."
    elif "help" in user_message:
        response = "I'm still in Phase 1, but I'm here."
    else:
        response = f"You said: {req.message}"

    return {"response": response}


@app.get("/")
def home():
    return {"status": "Ori backend is running"}

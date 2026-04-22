from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="Ori Backend - Phase 6 Streaming")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST ----------------
class ChatRequest(BaseModel):
    message: str


# ---------------- TOOL + ROUTE (simple for now) ----------------
def process(message: str):
    msg = message.lower()

    if "hello" in msg:
        return "Hey 👋 I'm Ori streaming now..."

    if "calculate" in msg:
        try:
            expr = msg.replace("calculate", "")
            return f"The answer is {eval(expr)}"
        except:
            return "Math error"

    return f"I received: {message}"


# =========================
# 🧠 STREAM GENERATOR
# =========================
def stream_response(text: str):
    for char in text:
        yield char
        time.sleep(0.02)  # simulate streaming delay


# =========================
# 🧠 STREAM ENDPOINT
# =========================
@app.post("/chat")
def chat(req: ChatRequest):

    response = process(req.message)

    return StreamingResponse(
        stream_response(response),
        media_type="text/plain"
    )


# ---------------- HEALTH ----------------
@app.get("/")
def home():
    return {
        "status": "Ori backend running",
        "phase": 6,
        "system": "streaming enabled"
    }

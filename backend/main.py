from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ori Backend - Phase 2")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later in Phase 24
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODEL ----------------
class ChatRequest(BaseModel):
    message: str


# ---------------- PHASE 2 INTENT BRAIN ----------------
def detect_intent(message: str):
    msg = message.lower().strip()

    # greeting
    if any(word in msg for word in ["hello", "hi", "hey", "yo"]):
        return "greeting"

    # help
    if "help" in msg:
        return "help"

    # identity
    if "what are you" in msg or "who are you" in msg:
        return "identity"

    # basic math trigger
    if any(word in msg for word in ["calculate", "solve", "+", "-", "*", "/"]):
        return "math"

    # default
    return "general"


# ---------------- RESPONSE ENGINE ----------------
def generate_response(intent, message):

    if intent == "greeting":
        return "Hey 👋 I'm Ori. I'm starting to understand you better now."

    if intent == "help":
        return "I'm still early in development, but I can already understand your intent."

    if intent == "identity":
        return "I'm Ori — your modular AI system being built step by step."

    if intent == "math":
        try:
            expr = message.lower().replace("calculate", "").strip()
            return str(eval(expr))
        except:
            return "I couldn't safely calculate that."

    return f"I understood your message as general input: '{message}'. I'm learning how to handle this better."


# ---------------- MAIN CHAT ENDPOINT ----------------
@app.post("/chat")
def chat(req: ChatRequest):

    intent = detect_intent(req.message)
    response = generate_response(intent, req.message)

    return {
        "response": response,
        "intent": intent,
        "phase": 2
    }


# ---------------- HEALTH CHECK ----------------
@app.get("/")
def home():
    return {
        "status": "Ori backend running",
        "phase": 2
    }

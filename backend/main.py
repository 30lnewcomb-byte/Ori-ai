from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ori Backend - Phase 2")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock later in Phase 24
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODEL ----------------
class ChatRequest(BaseModel):
    message: str


# ---------------- PHASE 2: INTENT BRAIN ----------------
def detect_intent(message: str):
    msg = message.lower()

    # Greeting intent
    if any(word in msg for word in ["hello", "hi", "hey"]):
        return "greeting"

    # Help intent
    if "help" in msg:
        return "help"

    # Identity intent
    if "what are you" in msg or "who are you" in msg:
        return "identity"

    # Default
    return "general"


# ---------------- MAIN CHAT ENDPOINT ----------------
@app.post("/chat")
def chat(req: ChatRequest):
    message = req.message
    intent = detect_intent(message)

    if intent == "greeting":
        response = "Hey 👋 I'm Ori. I'm starting to understand you better now."

    elif intent == "help":
        response = "I'm still early in development, but I can already understand what you're trying to say."

    elif intent == "identity":
        response = "I'm Ori — your modular AI system being built step by step."

    elif intent == "general":
        response = f"I understood your message as general input: '{message}'. I'm learning how to handle this better."

    else:
        response = "Something unexpected happened in my brain layer."

    return {
        "response": response,
        "intent": intent
    }


# ---------------- HEALTH CHECK ----------------
@app.get("/")
def home():
    return {
        "status": "Ori backend running",
        "phase": 2
    }

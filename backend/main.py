from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ori Backend - Phase 3 Router")

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


# ---------------- ROUTER BRAIN ----------------
def route_message(message: str):
    msg = message.lower().strip()

    # ROUTE: GREETING
    if any(w in msg for w in ["hello", "hi", "hey"]):
        return "greeting"

    # ROUTE: MATH / TOOL
    if any(w in msg for w in ["calculate", "+", "-", "*", "/"]):
        return "tool_math"

    # ROUTE: IDENTITY
    if "who are you" in msg or "what are you" in msg:
        return "identity"

    # ROUTE: HELP
    if "help" in msg:
        return "help"

    # ROUTE: DEFAULT CHAT
    return "chat"


# ---------------- RESPONSE SYSTEMS ----------------
def handle_greeting():
    return "Hey 👋 I'm Ori. Now I'm running a router brain (Phase 3)."


def handle_identity():
    return "I'm Ori — a modular AI system with routing intelligence now active."


def handle_help():
    return "I can now route messages into different systems (chat, tools, logic)."


def handle_math(message):
    try:
        expr = message.lower().replace("calculate", "").strip()
        return str(eval(expr))
    except:
        return "I couldn't safely calculate that."


def handle_chat(message):
    return f"I routed this into general chat mode: '{message}'. I'm getting smarter."


# ---------------- MAIN ENDPOINT ----------------
@app.post("/chat")
def chat(req: ChatRequest):

    route = route_message(req.message)

    if route == "greeting":
        response = handle_greeting()

    elif route == "identity":
        response = handle_identity()

    elif route == "help":
        response = handle_help()

    elif route == "tool_math":
        response = handle_math(req.message)

    else:
        response = handle_chat(req.message)

    return {
        "response": response,
        "route": route,
        "phase": 3
    }


# ---------------- HEALTH ----------------
@app.get("/")
def home():
    return {
        "status": "Ori backend running",
        "phase": 3,
        "system": "router enabled"
    }

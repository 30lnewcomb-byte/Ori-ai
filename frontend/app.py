from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import math

app = FastAPI(title="Ori Backend - Phase 4 Tools")

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


# ---------------- ROUTER ----------------
def route_message(msg: str):
    msg = msg.lower()

    if any(x in msg for x in ["hello", "hi", "hey"]):
        return "greeting"

    if "calculate" in msg or any(op in msg for op in ["+", "-", "*", "/"]):
        return "tool_math"

    if "square root" in msg:
        return "tool_sqrt"

    if "who are you" in msg:
        return "identity"

    return "chat"


# ---------------- TOOLS ----------------
def tool_math(msg: str):
    try:
        expr = msg.lower().replace("calculate", "").strip()
        return str(eval(expr))
    except:
        return "Math error"

def tool_sqrt(msg: str):
    try:
        num = float(msg.lower().replace("square root", "").strip())
        return str(math.sqrt(num))
    except:
        return "Invalid number"


# ---------------- RESPONSE SYSTEM ----------------
def handle(route: str, msg: str):

    if route == "greeting":
        return "Hey 👋 I'm Ori (Phase 4 Tools active)."

    if route == "identity":
        return "I'm Ori — now with tool execution system enabled."

    if route == "tool_math":
        return tool_math(msg)

    if route == "tool_sqrt":
        return tool_sqrt(msg)

    return f"I handled this in chat mode: {msg}"


# ---------------- MAIN ENDPOINT ----------------
@app.post("/chat")
def chat(req: ChatRequest):

    route = route_message(req.message)
    response = handle(route, req.message)

    return {
        "response": response,
        "route": route,
        "phase": 4,
        "tool_mode": route.startswith("tool")
    }


# ---------------- HEALTH ----------------
@app.get("/")
def home():
    return {
        "status": "Ori backend running",
        "phase": 4,
        "system": "tools enabled"
    }

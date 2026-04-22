from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import math

app = FastAPI(title="Ori Backend - Phase 5 Tool Plugins")

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


# =========================
# 🧠 TOOL REGISTRY SYSTEM
# =========================
class Tool:
    def __init__(self, name, trigger, func):
        self.name = name
        self.trigger = trigger
        self.func = func


# ---------------- TOOLS ----------------
def math_tool(msg):
    expr = msg.lower().replace("calculate", "").strip()
    try:
        return str(eval(expr))
    except:
        return "Math error"


def sqrt_tool(msg):
    try:
        num = float(msg.lower().replace("square root", "").strip())
        return str(math.sqrt(num))
    except:
        return "Invalid number"


def echo_tool(msg):
    return f"Echo tool activated: {msg}"


# ---------------- REGISTER TOOLS ----------------
TOOLS = [
    Tool("math", lambda m: "calculate" in m or any(op in m for op in "+-*/"), math_tool),
    Tool("sqrt", lambda m: "square root" in m, sqrt_tool),
]


# =========================
# 🧠 ROUTER (PLUGIN BASED)
# =========================
def run_tools(message: str):
    msg = message.lower()

    for tool in TOOLS:
        if tool.trigger(msg):
            return {
                "result": tool.func(message),
                "tool": tool.name
            }

    return None


# =========================
# 🧠 NORMAL CHAT HANDLER
# =========================
def chat_handler(msg: str):
    return f"General chat mode: {msg}"


# =========================
# 🧠 MAIN ENDPOINT
# =========================
@app.post("/chat")
def chat(req: ChatRequest):

    tool_result = run_tools(req.message)

    if tool_result:
        return {
            "response": tool_result["result"],
            "route": "tool",
            "tool": tool_result["tool"],
            "phase": 5
        }

    response = chat_handler(req.message)

    return {
        "response": response,
        "route": "chat",
        "phase": 5
    }


# ---------------- HEALTH ----------------
@app.get("/")
def home():
    return {
        "status": "Ori backend running",
        "phase": 5,
        "system": "plugin tools enabled"
    }

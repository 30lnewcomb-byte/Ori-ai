import streamlit as st
import requests
import os

API_URL = os.getenv("ORI_API_URL", "https://ori-ai.onrender.com/chat")

st.set_page_config(page_title="Ori AI", layout="wide")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HEADER ----------------
st.markdown(
    "<h2 style='text-align:center;'>🧠 Ori AI</h2>",
    unsafe_allow_html=True
)

st.caption("Phase 3 Router System • Streamlit UI → Render Brain")

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:

    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])

    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
            st.caption(
                f"Route: {msg.get('route', 'unknown')} | Phase: {msg.get('phase', '?')}"
            )

# ---------------- INPUT ----------------
user_input = st.chat_input("Message Ori...")

if user_input:

    # show user message instantly
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # call backend
    try:
        res = requests.post(API_URL, json={"message": user_input})
        data = res.json()

        reply = data.get("response", "No response from Ori")
        route = data.get("route", "unknown")
        phase = data.get("phase", 3)

    except Exception as e:
        reply = "⚠️ Backend not reachable"
        route = "error"
        phase = 3

    # store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "route": route,
        "phase": phase
    })

    st.rerun()

import streamlit as st
import requests
import os

API_URL = os.getenv("ORI_API_URL", "https://ori-ai.onrender.com/chat")

st.set_page_config(page_title="Ori AI", layout="wide")

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- TITLE ----------------
st.markdown(
    "<h2 style='text-align:center;'>🧠 Ori AI</h2>",
    unsafe_allow_html=True
)

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])

    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
            st.caption(f"Intent: {msg.get('intent', 'unknown')}")

# ---------------- INPUT ----------------
user_input = st.chat_input("Message Ori...")

if user_input:

    # show user message immediately
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # call backend
    try:
        res = requests.post(API_URL, json={"message": user_input})
        data = res.json()

        reply = data.get("response", "No response")
        intent = data.get("intent", "unknown")

    except:
        reply = "⚠️ Backend not reachable"
        intent = "error"

    # store AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "intent": intent
    })

    st.rerun()

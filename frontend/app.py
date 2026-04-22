import streamlit as st
import requests
import time
import os

API_URL = os.getenv("ORI_API_URL", "https://ori-ai.onrender.com/chat")

st.set_page_config(page_title="Ori AI", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h2 style='text-align:center;'>🧠 Ori AI</h2>", unsafe_allow_html=True)

# ---------------- DISPLAY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            st.caption(f"Route: {msg.get('route')} | Phase: {msg.get('phase')}")

# ---------------- INPUT ----------------
user_input = st.chat_input("Message Ori...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking... 🤔")

        try:
            res = requests.post(API_URL, json={"message": user_input})
            data = res.json()

            response = data.get("response", "")
            route = data.get("route", "unknown")
            phase = data.get("phase", 4)

            # ---------------- STREAMING EFFECT ----------------
            streamed = ""
            for char in response:
                streamed += char
                time.sleep(0.01)
                placeholder.markdown(streamed)

        except:
            response = "⚠️ Backend not reachable"
            route = "error"
            phase = 4
            placeholder.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "route": route,
        "phase": phase
    })

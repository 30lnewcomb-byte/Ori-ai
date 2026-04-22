import streamlit as st
import requests
import os

API_URL = os.getenv("ORI_API_URL", "https://ori-ai.onrender.com/")

st.set_page_config(page_title="Ori AI", layout="wide")

# ---------------- CSS (ChatGPT-style feel) ----------------
st.markdown("""
<style>

.chat-container {
    max-width: 800px;
    margin: auto;
    padding-bottom: 100px;
}

.user-bubble {
    background-color: #2b2b2b;
    color: white;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: right;
}

.ori-bubble {
    background-color: #444654;
    color: white;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: left;
}

.intent-tag {
    font-size: 12px;
    opacity: 0.6;
    margin-top: 4px;
}

.title {
    text-align: center;
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HEADER ----------------
st.markdown("<div class='title'>🧠 Ori AI</div>", unsafe_allow_html=True)

# ---------------- CHAT DISPLAY ----------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class='user-bubble'>
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div class='ori-bubble'>
            {msg["content"]}
            <div class='intent-tag'>Intent: {msg.get("intent", "unknown")}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
user_input = st.text_input("Message Ori...", key="input")

col1, col2 = st.columns([1, 5])

with col1:
    send = st.button("Send")

# ---------------- SEND LOGIC ----------------
if send and user_input:

    # store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        res = requests.post(API_URL, json={"message": user_input})
        data = res.json()

        reply = data.get("response", "No response")
        intent = data.get("intent", "unknown")

    except:
        reply = "⚠️ Backend not reachable"
        intent = "error"

    # store Ori response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "intent": intent
    })

    st.rerun()

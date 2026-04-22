import streamlit as st
import requests
import os

# Local now → Render later (same code works both ways)
API_URL = os.getenv("ORI_API_URL", "http://localhost:8000/chat")

st.set_page_config(page_title="Ori AI", layout="centered")

st.title("🧠 Ori AI System (Phase 2)")

tab1, tab2 = st.tabs(["💬 Chat", "🔐 Backend Status"])

# ---------------- CHAT TAB ----------------
with tab1:

    st.subheader("Chat with Ori")

    if "history" not in st.session_state:
        st.session_state.history = []

    user_input = st.text_input("Type your message")

    if st.button("Send"):
        if user_input:
            try:
                res = requests.post(API_URL, json={"message": user_input})
                data = res.json()

                reply = data.get("response", "No response")
                intent = data.get("intent", "unknown")

            except:
                reply = "⚠️ Backend not reachable"
                intent = "error"

            st.session_state.history.append({
                "user": user_input,
                "ori": reply,
                "intent": intent
            })

    # Display chat history
    for item in st.session_state.history:
        st.markdown(f"**🧑 You:** {item['user']}")
        st.markdown(f"**🤖 Ori:** {item['ori']}")
        st.caption(f"🧠 Intent: {item['intent']}")
        st.markdown("---")


# ---------------- BACKEND TAB ----------------
with tab2:

    st.subheader("Backend Status")

    try:
        res = requests.get("http://localhost:8000/")
        st.success(res.json())
    except:
        st.error("Backend not running")

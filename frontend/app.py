import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"  # later change for Render

st.set_page_config(page_title="Ori AI", layout="centered")

tab1, tab2 = st.tabs(["💬 Chat", "🔐 API Panel"])

# ---------------- CHAT TAB ----------------
with tab1:
    st.title("Ori Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Type a message")

    if st.button("Send"):
        if user_input:
            # send to backend
            res = requests.post(API_URL, json={"message": user_input})
            reply = res.json()["response"]

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Ori", reply))

    # display chat
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 Ori:** {msg}")


# ---------------- API TAB ----------------
with tab2:
    st.title("API Panel")

    st.write("Backend Status Check:")

    try:
        res = requests.get("http://localhost:8000/")
        st.success(res.json())
    except:
        st.error("Backend not running")

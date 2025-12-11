import streamlit as st
from src.config.settings import BOT_NAME

def render_chat_interface():
    """Render chat interface"""

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    f"Halo saya {BOT_NAME}! Selamat datang di Starbucks. "
                    "Ada yang bisa saya bantu?"
                ),
            }
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message['content'])
    
    return st.chat_input("Ketik pertanyaan Anda di sini...")
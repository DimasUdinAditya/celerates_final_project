import streamlit as st

def render_sidebar():
    """Render sidebar with information"""
    with st.sidebar:
        # Baris untuk logo, pakai 3 kolom lalu taruh logo di tengah
        col_left, col_center, col_right = st.columns([1, 3, 1])
        with col_center:
            st.image(
                "https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/"
                "Starbucks_Corporation_Logo_2011.svg/1200px-"
                "Starbucks_Corporation_Logo_2011.svg.png",
                width=150,
            )

        st.markdown(
            "<h1 style='text-align: center;'>Starbucks Virtual Assistant</h1>",
            unsafe_allow_html=True, 
        )

        st.markdown("---")

        st.markdown("### 📋 Tentang")
        st.info(
            "Program ini menggunakan teknologi RAG (Retrieval-Augmented Generation) "
            "untuk menjawab pertanyaan tentang Starbucks berdasarkan dokumen yang dipelajari."
        )

        st.markdown("### 💡 Tips")
        st.markdown(
            """
            - Tanyakan tentang menu  
            - Tanyakan tentang promo  
            - Tanyakan tentang lokasi  
            - Tanyakan tentang kebijakan dan SOP 
            """
        )

        st.markdown("---")
        st.markdown("### ⚙️ Settings")

        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Halo! Selamat datang di Starbucks. Ada yang bisa saya bantu?",
                }
            ]
            # Jika Streamlit kamu belum mendukung st.rerun(), ganti dengan st.experimental_rerun()
            st.rerun()

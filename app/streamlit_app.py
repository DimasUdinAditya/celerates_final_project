import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from src.chains.retrieval_chain import create_rag_chain
from src.utils.validators import validate_query
from app.components.sidebar import render_sidebar
from app.components.chat_interface import render_chat_interface

st.set_page_config(
    page_title="Starbucks VA",
    page_icon="https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/1200px-Starbucks_Corporation_Logo_2011.svg.png",
    layout="wide"
)

def initialize_chain():
    """Initialize the RAG chain"""
    if "qa_chain" not in st.session_state:
        with st.spinner("Memuat sistem chatbot..."):
            try:
                st.session_state.qa_chain = create_rag_chain()
            except Exception as e:
                st.error(f"Error initializing chatbot: {str(e)}")
                st.exception(e)
                st.stop()

def main():
    """Main application"""
    
    render_sidebar()

    st.markdown(
        "<h1>Chat dengan Barista Virtual Starbucks</h1>",
        unsafe_allow_html=True,
    )
    
    st.markdown(
        "<p style='font-size: 0.95rem;'>"
        "Tanyakan menu, promo, atau informasi gerai, dan saya akan membantu Anda."
        "</p>",
        unsafe_allow_html=True,
    )
    
    initialize_chain()
    
    user_input = render_chat_interface()
    
    if user_input:
        is_valid, message = validate_query(user_input)
        
        if not is_valid:
            st.error(message)
            return
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Mencari jawaban..."):
                try:
                    response = st.session_state.qa_chain.invoke({"input": user_input})
                    
                    answer = response.get("answer", "Maaf, tidak ada jawaban tersedia.")
                    
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #FFFFFF;
                            border: 1px solid #E0E0E0;
                            border-radius: 12px;
                            border-left: 4px solid #00704A;
                            padding: 16px 20px;
                            margin-bottom: 10px;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                        ">
                            <p style="margin: 0; font-size: 0.95rem; line-height: 1.6;">
                                {answer}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    
                    # Show source documents (development purpose)
                    source_docs = response.get("source_documents", [])
                    if source_docs:
                        with st.expander("📚 Lihat sumber dokumen"):
                            for i, doc in enumerate(source_docs, 1):
                                st.markdown(f"**Sumber {i}:**")
                                st.text(doc.page_content[:200] + "...")
                                st.markdown("---")
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    error_msg = f"Maaf, terjadi kesalahan: {str(e)}"
                    st.error(error_msg)
                    st.exception(e)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
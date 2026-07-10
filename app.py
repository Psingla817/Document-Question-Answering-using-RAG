import os
import tempfile

import streamlit as st

from main import create_retriever, ask_question


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Document Question Answering using RAG",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False


# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------

st.markdown(
    """
<style>

.main{
    padding-top:20px;
}

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
}

.title{
    text-align:center;
    font-size:48px;
    font-weight:700;
    color:#1E3A8A;
}

.subtitle{
    text-align:center;
    font-size:18px;
    color:gray;
    margin-bottom:30px;
}

.info-card{
    background:#f8f9fa;
    padding:18px;
    border-radius:12px;
    border:1px solid #e6e6e6;
}

.status{
    color:green;
    font-weight:bold;
}

hr{
    margin-top:25px;
    margin-bottom:25px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.markdown(
    """
<div class="title">
📚 Document Question Answering using RAG
</div>

<div class="subtitle">
Upload any PDF and ask questions about its contents using Retrieval-Augmented Generation.
</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.title("📂 Document")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    st.divider()

    if uploaded_file is None:

        st.info("Upload a PDF to begin.")

    else:

        size = uploaded_file.size / (1024 * 1024)

        st.markdown("### 📄 Uploaded Document")

        st.markdown(
            f"""
<div class="info-card">

**Name**

{uploaded_file.name}

<br>

**Size**

{size:.2f} MB

<br>

**Status**

<span class="status">Ready for Processing</span>

</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    clear_chat = st.button(
        "🗑 Clear Chat",
        use_container_width=True
    )

    upload_new = st.button(
        "🔄 Upload Another PDF",
        use_container_width=True
    )


# ---------------------------------------------------
# Main Area Placeholder
# ---------------------------------------------------

chat_container = st.container()
        
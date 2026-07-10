import os
import tempfile

import streamlit as st

from main import create_retriever, ask_question


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# SESSION STATE
# =====================================================

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False

if "file_size" not in st.session_state:
    st.session_state.file_size = None


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
<style>

/* Main */

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
}


/* Header */

.main-title{

    font-size:38px;
    font-weight:800;
    color:#1D4ED8;
    text-align:center;
    margin-bottom:8px;

}

.sub-title{

    font-size:18px;
    color:#6B7280;
    text-align:center;
    margin-bottom:35px;

}


/* Sidebar */

section[data-testid="stSidebar"]{

    background:#F8FAFC;

}


/* Card */

.info-card{

    background:white;

    padding:18px;

    border-radius:14px;

    border:1px solid #E5E7EB;

    box-shadow:0 5px 15px rgba(0,0,0,0.05);

}


/* Buttons */

.stButton>button{

    width:100%;

    border-radius:10px;

    height:45px;

    font-weight:600;

}


/* Chat */

[data-testid="stChatMessage"]{

    border-radius:14px;

    padding:12px;

}


/* File Uploader */

[data-testid="stFileUploader"]{

    border-radius:12px;

}


/* Success */

.stSuccess{

    border-radius:10px;

}

.stInfo{

    border-radius:10px;

}

</style>
""",
    unsafe_allow_html=True,
)


# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
<div class="main-title">
📚 AI Document Assistant
</div>

<div class="sub-title">
Upload any PDF and ask questions using Retrieval-Augmented Generation (RAG)
</div>
""",
    unsafe_allow_html=True,
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📂 Document")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    st.divider()

    if uploaded_file is None:

        st.info(
            "Upload a PDF to begin."
        )

    else:

        size = uploaded_file.size/(1024*1024)

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

🟡 Ready for Processing

</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    clear_chat = st.button(
        "🗑 Clear Chat"
    )

    upload_new = st.button(
        "🔄 Upload Another PDF"
    )


# =====================================================
# METRICS
# =====================================================

col1,col2,col3 = st.columns(3)

with col1:

    st.metric(
        "Document",
        uploaded_file.name if uploaded_file else "-"
    )

with col2:

    if uploaded_file:

        st.metric(
            "Size",
            f"{uploaded_file.size/(1024*1024):.2f} MB"
        )

    else:

        st.metric(
            "Size",
            "-"
        )

with col3:

    st.metric(
        "Questions Asked",
        len(
            [
                m
                for m in st.session_state.messages
                if m["role"]=="user"
            ]
        )
    )


st.divider()


# =====================================================
# MAIN CHAT CONTAINER
# =====================================================

chat_container = st.container()

# =====================================================
# PROCESS DOCUMENT
# =====================================================

if uploaded_file is not None:

    if uploaded_file.name != st.session_state.current_file:

        st.session_state.current_file = uploaded_file.name
        st.session_state.messages = []

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_pdf:

            temp_pdf.write(uploaded_file.getvalue())
            pdf_path = temp_pdf.name

        progress = st.progress(0)

        with st.spinner("📚 Reading document..."):

            progress.progress(15)

            retriever = create_retriever(pdf_path)

            progress.progress(100)

        os.remove(pdf_path)

        st.session_state.retriever = retriever
        st.session_state.document_ready = True
        st.session_state.file_size = uploaded_file.size

        progress.empty()

        st.success("✅ Document processed successfully!")



# =====================================================
# CLEAR CHAT
# =====================================================

if clear_chat:

    st.session_state.messages = []

    st.rerun()



# =====================================================
# NEW DOCUMENT
# =====================================================

if upload_new:

    st.session_state.messages = []
    st.session_state.retriever = None
    st.session_state.current_file = None
    st.session_state.document_ready = False
    st.session_state.file_size = None

    st.rerun()



# =====================================================
# CHAT AREA
# =====================================================

with chat_container:

    if not st.session_state.document_ready:

        st.markdown("""
                    <div style="
                    padding:35px;
                    text-align:center;
                    border-radius:15px;
                    background:#F8FAFC;
                    border:1px solid #E5E7EB;
                    ">
                    <h2>👋 Welcome</h2>
                    <p style="font-size:18px;">
                    Upload a PDF from the sidebar.
                    </p>
                    <p style="margin-top:15px;">
                    After processing, you can ask unlimited questions about your document.
                    </p>
                    <p style="color:green;">
                    The assistant answers only from the uploaded document.
                    </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                    )

    else:

        st.success("🟢 Document Ready")

        st.markdown("### 💬 Conversation")

        st.markdown("---")

        # -------------------------
        # Previous Messages
        # -------------------------

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

        # -------------------------
        # Chat Input
        # -------------------------

        question = st.chat_input(
            "💬 Ask anything about your uploaded document..."
        )

        if question:

            # User Bubble

            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":question
                }
            )

            with st.chat_message("user"):

                st.markdown(question)

            # Assistant Bubble

            with st.chat_message("assistant"):

                with st.spinner("🤖 Thinking..."):

                    answer = ask_question(
                        st.session_state.retriever,
                        question
                    )

                    st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":answer
                }
            )
            
            # =====================================================
# FOOTER
# =====================================================

st.divider()

footer_left, footer_right = st.columns([4, 1])

with footer_left:

    st.caption(
        "📚 AI Document Assistant | Powered by Streamlit • LangChain • ChromaDB • Mistral AI"
    )

with footer_right:

    if st.session_state.document_ready:

        st.success("Ready")

    else:

        st.warning("Waiting")
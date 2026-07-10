import os
import tempfile

import streamlit as st

from main import create_retriever, ask_question


st.set_page_config(
    page_title="Book RAG Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Book Question Answering System")
st.write("Upload a PDF and ask questions about it.")

# -------------------------
# Session State
# -------------------------

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_file" not in st.session_state:
    st.session_state.current_file = None


# -------------------------
# Upload PDF
# -------------------------

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    # Only process if it's a NEW file
    if uploaded_file.name != st.session_state.current_file:

        st.session_state.current_file = uploaded_file.name

        # Clear previous chat
        st.session_state.messages = []

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_pdf:

            temp_pdf.write(uploaded_file.getvalue())
            pdf_path = temp_pdf.name

        with st.spinner("Processing document..."):

            retriever = create_retriever(pdf_path)

        st.session_state.retriever = retriever

        os.remove(pdf_path)

        st.success("Document processed successfully!")



# -------------------------
# Display Chat
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# -------------------------
# Chat Input
# -------------------------

if st.session_state.retriever is not None:

    question = st.chat_input(
        "Ask anything about your document..."
    )

    if question:

        # Display User Message

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # Generate Answer

        with st.spinner("Thinking..."):

            answer = ask_question(
                st.session_state.retriever,
                question
            )

        # Display Assistant Message

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

else:

    st.info("Upload a PDF to begin.")
        
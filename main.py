from dotenv import load_dotenv
import tempfile

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# -----------------------------
# Models (Loaded only once)
# -----------------------------

embeddings = MistralAIEmbeddings(
    model="mistral-embed"
)

llm = ChatMistralAI(
    model="mistral-small-2506"
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, reply exactly:

"I could not find the answer in the document."
"""
        ),
        (
            "human",
            """
Context:
{context}

Question:
{question}
"""
        )
    ]
)


# -------------------------------------------------------
# Create Retriever from Uploaded PDF
# -------------------------------------------------------

def create_retriever(pdf_path: str):

    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    # Temporary database (unique every upload)
    db_path = tempfile.mkdtemp()

    # Create Vector Store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10,
            "lambda_mult": 0.5,
        },
    )

    return retriever


# -------------------------------------------------------
# Ask Question
# -------------------------------------------------------

def ask_question(retriever, question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    messages = prompt.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(messages)

    return response.content


# -------------------------------------------------------
# Optional CLI Testing
# -------------------------------------------------------

if __name__ == "__main__":

    pdf_path = input("Enter PDF path: ")

    retriever = create_retriever(pdf_path)

    print("\nRAG Ready")
    print("Type 0 to exit\n")

    while True:

        question = input("Question: ")

        if question == "0":
            break

        answer = ask_question(retriever, question)

        print("\nAnswer:")
        print(answer)
        print()



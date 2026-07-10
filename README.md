# 📚 AI Document Assistant using RAG

A Retrieval-Augmented Generation (RAG) based application that allows users to upload any PDF document and ask natural language questions about its contents. The application retrieves relevant information from the uploaded document using semantic search and generates accurate responses using Mistral AI.

---

## ✨ Features

- 📄 Upload any PDF document
- 🔍 Automatic document parsing and chunking
- 🧠 Semantic search using Chroma Vector Database
- 🤖 AI-powered question answering with Mistral AI
- 💬 Continuous conversational interface
- 🔄 Upload a new document without restarting the application
- 🗑️ Clear chat history
- 🎨 Modern Streamlit-based user interface
- ✅ Answers generated only from the uploaded document

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- ChromaDB
- Mistral AI
- PyPDFLoader

---

## 📂 Project Structure

```text
Document-Question-Answering-using-RAG
│
├── app.py               # Streamlit UI
├── main.py              # RAG pipeline
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Psingla817/Document-Question-Answering-using-RAG.git
```

### 2. Navigate to the project

```bash
cd Document-Question-Answering-using-RAG
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

##
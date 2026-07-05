# 🤖 AI KnowledgeHub – Web RAG Chatbot

## 📌 Project Overview

AI KnowledgeHub is a **Retrieval-Augmented Generation (RAG)** based chatbot that allows users to chat with the content of any website.

The user provides a website URL, and the system automatically crawls the website, extracts its content, processes it into searchable knowledge, stores it in a vector database, and answers questions using **Llama 3**. The chatbot responds **only from the ingested website content**, ensuring accurate and context-aware answers.

---

# ✨ Features

* 🌐 Recursive website crawling
* 📄 HTML parsing and clean text extraction
* ✂️ Intelligent text chunking
* 🔢 Embedding generation using Sentence Transformers
* 🗄️ Vector storage with ChromaDB
* 🔍 Semantic similarity search
* 🤖 AI-powered answers using Llama 3 (Ollama)
* 🔒 Strict Retrieval-Augmented Generation (RAG)
* 🌍 Multi-website support with isolated collections
* 💬 Interactive Streamlit chatbot interface
* ⚡ FastAPI backend APIs

---

# 🛠️ Tech Stack

| Technology                               | Purpose                       |
| ---------------------------------------- | ----------------------------- |
| Python                                   | Core programming language     |
| FastAPI                                  | Backend REST APIs             |
| Streamlit                                | Frontend user interface       |
| Ollama                                   | Local LLM inference           |
| Llama 3                                  | Large Language Model          |
| ChromaDB                                 | Vector database               |
| Sentence Transformers (all-MiniLM-L6-v2) | Embedding generation          |
| BeautifulSoup                            | HTML parsing                  |
| Requests                                 | Website crawling              |
| LangChain                                | Text chunking & RAG utilities |

---

# 🧠 System Architecture

```text
User enters Website URL
        │
        ▼
Website Crawling
        │
        ▼
HTML Parsing
        │
        ▼
Text Cleaning
        │
        ▼
Text Chunking
        │
        ▼
Embedding Generation
        │
        ▼
Store Embeddings in ChromaDB
        │
───────────────────────────────────────
        │
User asks a Question
        │
        ▼
Semantic Retrieval
        │
        ▼
Relevant Context
        │
        ▼
Llama 3 (Ollama)
        │
        ▼
AI Generated Answer
```

---

# 📂 Project Structure

```text
AI-KnowledgeHub/
│
├── backend/
│   ├── app.py
│   ├── crawler.py
│   ├── parser.py
│   ├── scraper.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vectordb.py
│   ├── retrieval.py
│   ├── rag_pipeline.py
│   ├── llm.py
│   └── ingest_url.py
│
├── frontend.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Requirements

Before running the project, ensure you have:

* Python 3.10 or later
* Ollama installed
* Llama 3 model downloaded in Ollama
* Internet connection (for website crawling)

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/midhun222/AI-KnowledgeHub-Web-RAG-Bot.git
cd AI-KnowledgeHub-Web-RAG-Bot
```

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Start the FastAPI Backend

```bash
uvicorn backend.app:app --reload
```

Backend API will be available at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## Start the Streamlit Frontend

```bash
streamlit run frontend/frontend.py```

---

# 🔌 API Endpoints

| Endpoint  | Method | Description                                       |
| --------- | ------ | ------------------------------------------------- |
| `/ingest` | POST   | Crawl a website and store its content in ChromaDB |
| `/ask`    | POST   | Ask questions about the ingested website          |

---

# 💡 Example Workflow

1. Launch the backend server.
2. Launch the Streamlit frontend.
3. Enter a website URL.
4. Click **Ingest Website**.
5. Wait until ingestion is completed.
6. Ask questions such as:

   * What is this website about?
   * Summarize the main content.
   * Explain the key features.
7. Receive answers generated only from the ingested website.

---

# 🔒 RAG Design Principles

This project follows strict Retrieval-Augmented Generation principles.

* Only ingested website content is used for answering.
* External knowledge from the LLM is minimized.
* Each website is stored in its own vector collection.
* Semantic retrieval is performed before answer generation.
* Prevents cross-website knowledge contamination.

---

# 🎯 Learning Outcomes

This project demonstrates:

* End-to-end RAG pipeline implementation
* Website crawling and content extraction
* Text preprocessing and chunking
* Embedding generation
* Vector database integration
* Semantic retrieval
* LLM integration using Ollama
* FastAPI backend development
* Streamlit frontend development
* Full-stack AI application development

---

# 👨‍💻 Author

**Midhun NS**

---

# 📌 Project Status

* ✅ Project Completed
* ✅ Fully Functional
* ✅ Tested Locally
* ✅ Ready for Demonstration

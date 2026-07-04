from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.ingest_url import ingest_url
from backend.rag_pipeline import answer_question

# =====================================================
# FASTAPI APP
# =====================================================
app = FastAPI(
    title="AI KnowledgeHub",
    description="RAG Powered Website Chatbot",
    version="1.0.0"
)

# =====================================================
# CORS
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# REQUEST MODELS
# =====================================================
class QueryRequest(BaseModel):
    question: str
    url: str   # 🔥 IMPORTANT FIX


class URLRequest(BaseModel):
    url: str


# =====================================================
# HEALTH CHECK
# =====================================================
@app.get("/")
def home():
    return {
        "message": "AI KnowledgeHub Running 🚀",
        "status": "OK"
    }


# =====================================================
# INGEST URL
# =====================================================
@app.post("/ingest")
def ingest(req: URLRequest):
    try:
        count = ingest_url(req.url)

        return {
            "message": "URL ingested successfully",
            "chunks_stored": count,
            "url": req.url
        }

    except Exception as e:
        return {"error": str(e)}


# =====================================================
# ASK QUESTION (FIXED RAG FLOW)
# =====================================================
@app.post("/ask")
def ask(req: QueryRequest):

    try:
        answer = answer_question(req.question, req.url)  # 🔥 FIXED

        return {
            "question": req.question,
            "url": req.url,
            "answer": answer
        }

    except Exception as e:
        return {
            "error": str(e)
        }
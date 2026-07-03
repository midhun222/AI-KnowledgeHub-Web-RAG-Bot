from sentence_transformers import SentenceTransformer
import os

# ==============================
# SAFE ENV SETTINGS
# ==============================
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# ==============================
# MODEL CONFIG
# ==============================
MODEL_NAME = "all-MiniLM-L6-v2"

# ==============================
# LOAD MODEL (ONCE ONLY)
# ==============================
try:
    model = SentenceTransformer(
        MODEL_NAME,
        cache_folder="./models"
    )
    print("✅ Embedding model loaded successfully")

except Exception as e:
    print("❌ Model loading failed:", e)
    raise RuntimeError("Embedding model could not be loaded") from e


# ==============================
# CREATE EMBEDDINGS (FINAL FIX)
# ==============================
def create_embeddings(chunks: list):
    """
    Convert text chunks into embeddings
    """

    if not chunks:
        return []

    embeddings = model.encode(
        chunks,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return [
        {
            "text": chunk,
            "embedding": embedding.tolist()
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]


# ==============================
# QUERY EMBEDDING
# ==============================
def embed_query(query: str):
    """
    Convert query into embedding vector
    """

    return model.encode(
        query,
        normalize_embeddings=True
    ).tolist()
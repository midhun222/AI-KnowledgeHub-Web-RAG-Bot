import chromadb
import hashlib
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "chroma_db")

client = chromadb.PersistentClient(path=DB_PATH)


# =====================================================
# COLLECTION NAME
# =====================================================
def get_collection_name(source_url: str):
    return "kb_" + hashlib.md5(source_url.encode()).hexdigest()


def get_collection(source_url: str):
    return client.get_or_create_collection(
        name=get_collection_name(source_url)
    )


# =====================================================
# DOCUMENT ID
# =====================================================
def make_id(text: str, source_url: str):
    return hashlib.md5((text + source_url).encode()).hexdigest()


# =====================================================
# STORE EMBEDDINGS
# =====================================================
def store_embeddings(embedded_chunks, source_url):

    collection = get_collection(source_url)

    documents = []
    embeddings = []
    ids = []
    metadatas = []

    for item in embedded_chunks:

        text = item.get("text")
        embedding = item.get("embedding")

        if not text or embedding is None:
            continue

        documents.append(text)
        embeddings.append(embedding)
        ids.append(make_id(text, source_url))
        metadatas.append({
            "source": source_url
        })

    if not documents:
        return 0

    # Remove only duplicate IDs
    try:
        collection.delete(ids=ids)
    except Exception:
        pass

    time.sleep(0.1)

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✅ Stored {len(documents)} chunks for {source_url}")

    return len(documents)


# =====================================================
# SEARCH
# =====================================================
def search_similar_chunks(query_embedding, source_url, top_k=5):

    collection = get_collection(source_url)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "distances", "metadatas"]
    )

    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    retrieved_chunks = []

    for doc, dist, meta in zip(documents, distances, metadatas):

        if not doc:
            continue

        retrieved_chunks.append({
            "text": doc.strip(),
            "score": float(dist),
            "source": meta.get("source", "unknown") if meta else "unknown"
        })

    retrieved_chunks.sort(key=lambda x: x["score"])

    return retrieved_chunks
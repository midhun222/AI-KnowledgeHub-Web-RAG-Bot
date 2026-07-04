import chromadb
import hashlib

from backend.embeddings import embed_query

# =====================================================
# CHROMA CLIENT
# =====================================================
client = chromadb.PersistentClient(path="./chroma_db")


# =====================================================
# SAME COLLECTION NAME AS vectordb.py
# =====================================================
def get_collection_name(source_url: str):
    return "kb_" + hashlib.md5(source_url.encode()).hexdigest()


def get_collection(source_url: str):

    if not source_url:
        raise ValueError("source_url cannot be empty")

    return client.get_or_create_collection(
        name=get_collection_name(source_url)
    )


# =====================================================
# SEARCH
# =====================================================
def search_similar_chunks(query: str, source_url: str, top_k: int = 5):

    try:

        print(f"\n🔍 Searching website: {source_url}")

        query_embedding = embed_query(query)

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
                "source": meta.get("source", source_url)
            })

        retrieved_chunks.sort(key=lambda x: x["score"])

        print("\n========== RETRIEVED CHUNKS ==========")

        if not retrieved_chunks:
            print("No chunks found.")

        for i, chunk in enumerate(retrieved_chunks, start=1):
            print(f"{i}. score={chunk['score']}")
            print(chunk["text"][:200])
            print()

        print("======================================\n")

        return retrieved_chunks

    except Exception as e:
        print("❌ Retrieval Error:", str(e))
        return []
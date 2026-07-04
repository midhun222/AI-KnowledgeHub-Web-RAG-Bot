from backend.llm import generate_answer
from backend.retrieval import search_similar_chunks


def answer_question(query: str, url: str = None):

    # =========================
    # CHECK URL
    # =========================
    if not url:
        return "No website has been ingested. Please ingest a website first."

    print(f"\n🔍 Searching website: {url}")

    # =========================
    # RETRIEVE DOCUMENTS
    # =========================
    docs = search_similar_chunks(query, url)

    print("\n========== RETRIEVED DOCUMENTS ==========")

    if not docs:
        print("No matching documents found.")
        return "The answer is not available in the provided website."

    for i, doc in enumerate(docs, start=1):
        print(f"{i}. Source: {doc['source']}")
        print(doc["text"][:200])
        print()

    # =========================
    # SORT BY SCORE
    # =========================
    docs = sorted(docs, key=lambda x: x["score"])[:8]

    # =========================
    # BUILD CONTEXT
    # =========================
    context_parts = []

    for doc in docs:
        context_parts.append(
            f"SOURCE: {doc['source']}\n{doc['text']}"
        )

    context = "\n\n".join(context_parts)

    print("\n========== FINAL CONTEXT ==========")
    print(context[:1000])
    print("==================================\n")

    # =========================
    # PROMPT
    # =========================
    prompt = f"""
You are a strict Retrieval-Augmented Generation (RAG) assistant.

RULES:
- Answer ONLY from the context below.
- Never use your own knowledge.
- If the answer is not present in the context, reply exactly:
"The answer is not available in the provided website."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    # =========================
    # LLM
    # =========================
    return generate_answer(prompt).strip()
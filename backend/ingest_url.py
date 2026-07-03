import time
from backend.crawler import crawl_website
from backend.chunker import split_text
from backend.embeddings import create_embeddings
from backend.vectordb import store_embeddings


# =====================================================
# CLEAN + FILTER CHUNKS
# =====================================================
def clean_chunks(chunks: list):

    cleaned = []

    for c in chunks:
        if not c:
            continue

        c = c.strip()

        # remove very small chunks
        if len(c) < 80:
            continue

        # remove junk/navigation text
        junk_words = [
            "edit", "wikimedia", "jump to", "contents",
            "talk", "upload file", "cite this", "navigation",
            "cookie", "privacy policy", "terms of use"
        ]

        if any(word in c.lower() for word in junk_words):
            continue

        cleaned.append(c)

    # Remove duplicates while preserving order
    seen = set()
    unique_chunks = []

    for c in cleaned:
        if c not in seen:
            unique_chunks.append(c)
            seen.add(c)

    return unique_chunks


# =====================================================
# MAIN INGESTION PIPELINE
# =====================================================
def ingest_url(url: str):

    try:
        start_time = time.time()

        print(f"\n🚀 Crawling website: {url}")

        pages = crawl_website(url)

        if not pages:
            print("❌ No pages scraped")
            return 0

        full_text = "\n".join(pages)

        if len(full_text.strip()) < 150:
            print("❌ Not enough content scraped")
            return 0

        print(f"📄 Total text length: {len(full_text)}")

        # =========================
        # CHUNKING
        # =========================
        print("\n✂️ Splitting text into chunks...")
        chunks = split_text(full_text)

        if not chunks:
            print("❌ Chunking failed")
            return 0

        print(f"📦 Raw chunks: {len(chunks)}")

        # =========================
        # CLEANING
        # =========================
        print("\n🧹 Cleaning chunks...")
        chunks = clean_chunks(chunks)

        if not chunks:
            print("❌ No valid chunks after cleaning")
            return 0

        print(f"✅ Clean chunks: {len(chunks)}")

        # =========================
        # EMBEDDINGS
        # =========================
        print("\n🔢 Creating embeddings...")

        embedded_chunks = create_embeddings(chunks)

        if not embedded_chunks:
            print("❌ No embeddings generated")
            return 0

        # =========================
        # STORE IN VECTOR DB
        # =========================
        print("\n💾 Storing in ChromaDB...")

        count = store_embeddings(embedded_chunks, url)

        end_time = time.time()

        print(f"\n✅ Stored {count} chunks successfully")
        print(f"⏱ Time taken: {round(end_time - start_time, 2)} sec")

        return count

    except Exception as e:
        print("\n🔥 INGESTION ERROR:", str(e))
        return 0
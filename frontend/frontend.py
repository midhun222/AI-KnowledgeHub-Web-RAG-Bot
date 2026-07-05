import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000"

# =====================================================
# 🎨 CUSTOM THEME (MODERN DARK UI)
# =====================================================
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Title */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #6C63FF;
}

/* Subtitle */
.sub-title {
    font-size: 18px;
    color: #AAB0C5;
}

/* Chat bubbles */
.chat-box {
    background-color: #1A1D24;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #2A2D36;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #11141B;
}

/* Buttons */
.stButton > button {
    background-color: #6C63FF;
    color: white;
    border-radius: 8px;
}

.stButton > button:hover {
    background-color: #5146d8;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE (MEMORY)
# =====================================================
if "websites" not in st.session_state:
    st.session_state.websites = 0

if "chunks" not in st.session_state:
    st.session_state.chunks = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

if "active_url" not in st.session_state:
    st.session_state.active_url = None

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="AI KnowledgeHub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# MAIN TITLE
# =====================================================
st.markdown('<div class="main-title">🧠 AI KnowledgeHub</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="sub-title">🚀 RAG Powered Website Chatbot </div>',
    unsafe_allow_html=True
)

st.markdown("---")

# =====================================================
# DASHBOARD METRICS
# =====================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🌐 Websites", st.session_state.websites)

with col2:
    st.metric("📄 Chunks", st.session_state.chunks)

with col3:
    st.metric("🧠 Model", "Llama3")

with col4:
    st.metric("⚡ Status", "Ready")

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.title("🧠 AI KnowledgeHub")
    st.markdown("---")

    st.subheader("🌐 Website Ingestion")

    url = st.text_input("Website URL", placeholder="https://example.com")

    ingest_btn = st.button("🚀 Ingest Website", use_container_width=True)

    st.markdown("---")

    st.subheader("💡 Suggested Questions")

    if st.button("What is this website about?"):
        st.session_state.messages.append({
            "role": "user",
            "content": "What is this website about?"
        })

    if st.button("Summarize the website"):
        st.session_state.messages.append({
            "role": "user",
            "content": "Summarize this website"
        })

    if st.button("What are the main features?"):
        st.session_state.messages.append({
            "role": "user",
            "content": "What are the main features?"
        })

    st.markdown("---")

    st.subheader("📊 System")
    st.success("LLM : Llama3")
    st.info("Embeddings : MiniLM")
    st.write("Version : 1.0")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.session_state.last_sources = []
        st.success("Chat cleared!")

    # INGEST
    if ingest_btn:

        if not url:
            st.warning("Please enter a website URL.")

        else:
            try:
                with st.spinner("🔄 Ingesting website..."):
                    start = time.time()

                    res = requests.post(
                        f"{API_URL}/ingest",
                        json={"url": url}
                    )

                    end = time.time()

                if res.status_code == 200:

                    data = res.json()

                    st.success("✅ Website ingested successfully!")
                    st.json(data)

                    st.session_state.websites += 1
                    st.session_state.chunks = data.get("chunks_stored", 0)
                    st.session_state.active_url = url
                    st.info(f"⏱ Done in {end-start:.2f} sec")

                else:
                    st.error(res.text)

            except Exception as e:
                st.error(f"Request failed: {e}")

# =====================================================
# CHAT SECTION
# =====================================================
st.subheader("💬 Chat with your Knowledge Base")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div class='chat-box'>{msg['content']}</div>", unsafe_allow_html=True)

question = st.chat_input("Ask something about the website...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(f"<div class='chat-box'>{question}</div>", unsafe_allow_html=True)

    try:
        with st.spinner("🤔 Thinking..."):

            start = time.time()

            res = requests.post(
                f"{API_URL}/ask",
                json={
                    "question": question,
                    "url": st.session_state.active_url
                }
            )

            end = time.time()

        if res.status_code == 200:

            data = res.json()
            answer = data.get("answer", "")
            sources = data.get("sources", [])

            st.session_state.last_sources = sources

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            with st.chat_message("assistant"):
                st.markdown(f"""
                <div class='chat-box'>
                🤖 <b>Answer</b><br><br>
                {answer}
                </div>
                """, unsafe_allow_html=True)

            st.caption(f"Answered in {end-start:.2f} sec")

        else:
            st.error(res.text)

    except Exception as e:
        st.error(f"Request failed: {e}")

# =====================================================
# SOURCES
# =====================================================
if st.session_state.last_sources:

    st.markdown("---")
    st.subheader("📚 Sources Used (RAG Evidence)")

    for i, src in enumerate(st.session_state.last_sources):

        with st.expander(f"Source {i+1}"):
            st.write(src)
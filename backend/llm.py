import ollama

MODEL_NAME = "llama3"


def generate_answer(prompt: str) -> str:
    try:
        print("\n🔥 LLM REQUEST STARTED")

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict RAG assistant. "
                        "Only use provided context. "
                        "If answer is missing, say: "
                        "'Information not available in the provided context.'"
                    ),
                },
                {
                    "role": "user",
                    "content": prompt[:6000],  # 🔥 prevent overload crash
                },
            ],
            options={
                "temperature": 0.2,
                "top_p": 0.9,
            },
        )

        print("🔥 LLM RESPONSE RECEIVED")

        # SAFE EXTRACTION (IMPORTANT FIX)
        if "message" in response and "content" in response["message"]:
            return response["message"]["content"].strip()

        return "No valid response from LLM"

    except Exception as e:
        return f"LLM Error: {str(e)}"
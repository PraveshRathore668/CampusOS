import os
from google import genai
from google.genai import types

_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """You are a helpful campus assistant. Answer the student's question using ONLY the context provided below.

If the context does not contain enough information to answer the question, respond exactly with: "I couldn't find this information in the available campus documents."

Do not use any outside knowledge. Do not make up information."""


def generate_answer(question: str, context_chunks: list[str]) -> str:
    context_text = "\n\n---\n\n".join(context_chunks)

    user_message = f"""Context from campus documents:
{context_text}

Question: {question}"""

    response = _client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=500,
        ),
    )

    return response.text

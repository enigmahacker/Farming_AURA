import os
import json
from typing import Dict
from . import knowledge

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


async def ask_assistant(payload: Dict) -> str:
    """Ask the AI assistant. This function supports retrieval-augmented answers using JSON-trained knowledge.

    Flow:
    - Load relevant knowledge via a simple retriever (`backend/app/knowledge.py`).
    - If OPENAI_API_KEY is set, call the OpenAI chat completion API and instruct it to answer in Hindi.
    - Otherwise, return a Hindi-friendly fallback composed from matched snippets.
    """
    message = payload.get("message", "")
    context = payload.get("context", {}) or {}

    # Try retrieval from knowledge index
    hits = knowledge.query_knowledge(message, top_k=3)

    # If we have OpenAI available, build a prompt that prefers Hindi and supplies the retrieved context
    if OPENAI_API_KEY:
        try:
            import openai
            openai.api_key = OPENAI_API_KEY
            system = (
                "You are Farming_AURA assistant. Answer concisely and in farmer-friendly Hindi. "
                "When provided with knowledge snippets, use them to ground your answer and cite if needed."
            )
            # Build context text
            context_text = "\n\n".join([f"Title: {h.get('title')}\nContent: {h.get('text')}" for h in hits]) if hits else ""
            user_prompt = f"{message}\n\nUse the following knowledge to answer in Hindi:\n{context_text}\n\nAnswer in Hindi. Keep it short and actionable."
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt}
            ]
            res = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, max_tokens=400)
            text = res["choices"][0]["message"]["content"]
            return text
        except Exception as e:
            return f"क्षमा करें, असिस्टेंट अस्थायी रूप से उपलब्ध नहीं है: {str(e)}"

    # No OpenAI: return concatenated matched snippets in Hindi if available; otherwise simple Hindi fallback
    if hits:
        parts = []
        for h in hits:
            lang = h.get("lang", "hi")
            content = h.get("text", "")
            if lang == "hi":
                parts.append(content)
            else:
                parts.append(content)
        # Combine into a short Hindi header + snippets
        header = "मैंने निम्नलिखित जानकारी मिली — कृपया नीचे देखें:"  # Hindi
        return header + "\n\n" + "\n\n---\n\n".join(parts)

    # Minimal Hindi fallback
    return "माफ़ कीजिए, असिस्टेंट अभी उपलब्ध नहीं है। कृपया बाद में पुनः प्रयास करें या अपना प्रश्न और विस्तार से बताइए।"

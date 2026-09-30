"""Utility & helper functions."""
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langsearch.config import settings


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_gemini_chat_model() -> ChatGoogleGenerativeAI:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    model = ChatGoogleGenerativeAI(
            model= settings.GOOGLE_GEMINI_MODEL_NAME,
            temperature=0.2,
            top_p=0.85,
            timeout=200.0,  # 200 seconds timeout for complex requests
            max_retries=2,  # Retry up to 2 times on failure
            google_api_key=settings.GOOGLE_GEMINI_API_KEY,
        )
    return model

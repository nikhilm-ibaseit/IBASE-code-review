"""Local LLM config for LiteLLM (Ollama OpenAI-compatible API)."""

import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_MODEL: str = os.getenv("OPENAI_MODEL") or "openai/llama3.2:3b"
OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE") or "http://localhost:11434/v1"
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") or "ollama"


def get_local_llm():
    from google.adk.models.lite_llm import LiteLlm

    return LiteLlm(
        model=OPENAI_MODEL,
        api_base=OPENAI_API_BASE,
        api_key=OPENAI_API_KEY,
    )

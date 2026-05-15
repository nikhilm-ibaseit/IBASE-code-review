"""LiteLLM config for OpenAI-compatible APIs (hackathon endpoint or Ollama)."""

import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_MODEL: str = os.getenv("OPENAI_MODEL") or "openai/agent-strong"
OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE") or "https://9122-202-153-40-242.ngrok-free.app/v1"
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") or ""


def get_local_llm():
    from google.adk.models.lite_llm import LiteLlm

    return LiteLlm(
        model=OPENAI_MODEL,
        api_base=OPENAI_API_BASE,
        api_key=OPENAI_API_KEY,
    )

#choisisant le modéle a utiliser
import os
from .base import LLMProvider
from .gemini_adapter import GeminiAdapter


# from .openai_adapter import OpenAIAdapter

def get_llm() -> LLMProvider:
    provider = os.getenv("LLM_PROVIDER", "gemini")

    if provider == "gemini":
        return GeminiAdapter()
    # elif provider == "openai":
    #     return OpenAIAdapter()
    else:
        raise ValueError(f"Fournisseur LLM inconnu : {provider}")
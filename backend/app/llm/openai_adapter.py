import os
from openai import OpenAI
from .base import LLMProvider
from typing import Any, Dict, Optional


class OpenAIAdapter(LLMProvider):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("LLM_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 schema: Optional[Dict[str, Any]] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {"model": self.model, "messages": messages}
        if schema:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
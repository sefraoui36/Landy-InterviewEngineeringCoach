import os
from google import genai
from google.genai import types
from .base import LLMProvider
from typing import Any, Dict, Optional


class GeminiAdapter(LLMProvider):
    def __init__(self):
        # The new SDK client automatically picks up the GEMINI_API_KEY env var,
        # but we pass it explicitly for consistency with your .env setup.
        self.client = genai.Client(api_key=os.getenv("LLM_API_KEY"))
        self.model_name = os.getenv("LLM_MODEL", "gemini-2.0-flash")

    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 schema: Optional[Dict[str, Any]] = None) -> str:
        # Build the configuration for the model
        config = types.GenerateContentConfig()

        if system_prompt:
            config.system_instruction = system_prompt

        if schema:
            # Force the model to output JSON that matches your schema
            config.response_mime_type = "application/json"
            config.response_json_schema = schema

        # Generate the content
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config
        )

        return response.text
"""
LLM Client - OpenAI-compatible API wrapper
"""

import os
from typing import List, Dict, Generator, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """OpenAI-compatible LLM client wrapper."""

    def __init__(self):
        self.api_base = os.environ.get("LLM_API_BASE", "http://localhost:11434/v1")
        self.api_key = os.environ.get("LLM_API_KEY", "not-needed")
        self.model = os.environ.get("LLM_MODEL", "qwen2.5:7b")

        self.client = OpenAI(base_url=self.api_base, api_key=self.api_key)

    @property
    def config(self) -> Dict[str, str]:
        """Return current configuration."""
        return {"api_base": self.api_base, "model": self.model}

    def test_connection(self) -> bool:
        """Test connection to LLM endpoint."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5,
            )
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def chat(
        self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None
    ) -> str:
        """Send chat messages and return full response."""
        full_messages = []

        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})

        full_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=self.model, messages=full_messages
        )

        return response.choices[0].message.content

    def stream_chat(
        self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        """Send chat messages and yield response chunks."""
        full_messages = []

        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})

        full_messages.extend(messages)

        stream = self.client.chat.completions.create(
            model=self.model, messages=full_messages, stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

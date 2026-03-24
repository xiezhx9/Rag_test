"""
Embedding Model - Remote API (OpenAI-compatible)
"""

import os
from typing import List
import httpx
from dotenv import load_dotenv

load_dotenv()


class EmbeddingModel:
    """Remote embedding model wrapper (OpenAI-compatible API)."""

    def __init__(self):
        self.api_base = os.environ.get(
            "EMBEDDING_API_BASE", "http://localhost:11434/v1"
        )
        self.api_key = os.environ.get("EMBEDDING_API_KEY", "not-needed")
        self.model_name = os.environ.get("EMBEDDING_MODEL", "nomic-embed-text")
        self._dimension = None

        # HTTP client
        self.client = httpx.Client(timeout=60.0)

        # Determine API URL - check if api_base already contains /embeddings
        if self.api_base.rstrip("/").endswith("/embeddings"):
            self.api_url = self.api_base
        else:
            self.api_url = f"{self.api_base.rstrip('/')}/embeddings"

    @property
    def dimension(self) -> int:
        """Return embedding dimension."""
        if self._dimension is None:
            # Get dimension from a test embedding
            test_embedding = self.embed_query("test")
            self._dimension = len(test_embedding)
        return self._dimension

    def _get_embedding(self, text: str) -> List[float]:
        """Call embedding API and return the embedding vector."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {"model": self.model_name, "input": text}

        try:
            response = self.client.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            return data["data"][0]["embedding"]

        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Embedding API error: {e.response.status_code} - {e.response.text}"
            )
        except Exception as e:
            raise RuntimeError(f"Embedding API request failed: {e}")

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text.

        Args:
            text: Query text to embed

        Returns:
            List of floats representing the embedding
        """
        if not text:
            text = " "  # Handle empty input

        return self._get_embedding(text)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple texts in batch.

        Args:
            texts: List of texts to embed

        Returns:
            List of embeddings (each is a list of floats)
        """
        if not texts:
            return []

        # Handle empty strings
        texts = [t if t else " " for t in texts]

        # Batch request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {"model": self.model_name, "input": texts}

        try:
            response = self.client.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            # Sort by index to ensure correct order
            embeddings_data = sorted(data["data"], key=lambda x: x["index"])
            return [item["embedding"] for item in embeddings_data]

        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Embedding API error: {e.response.status_code} - {e.response.text}"
            )
        except Exception as e:
            raise RuntimeError(f"Embedding API request failed: {e}")

    def __del__(self):
        """Cleanup HTTP client."""
        if hasattr(self, "client"):
            self.client.close()

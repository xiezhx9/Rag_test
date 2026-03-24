"""
Document Processor - Markdown parsing and chunking
"""

import os
import re
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class DocumentProcessor:
    """Process Markdown documents into chunks."""

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or int(os.environ.get("CHUNK_SIZE", "512"))
        self.chunk_overlap = chunk_overlap or int(os.environ.get("CHUNK_OVERLAP", "50"))

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove excessive whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r" {2,}", " ", text)
        return text.strip()

    def _split_into_chunks(self, text: str, source_file: str) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks."""
        text = self._clean_text(text)

        if len(text) <= self.chunk_size:
            return [{"text": text, "source_file": source_file, "chunk_index": 0}]

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + self.chunk_size

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending punctuation
                last_period = text.rfind("。", start, end)
                last_newline = text.rfind("\n", start, end)
                last_space = text.rfind(" ", start, end)

                # Prefer breaking at sentence or paragraph boundary
                break_point = max(last_period, last_newline)
                if break_point > start + self.chunk_size // 2:
                    end = break_point + 1
                elif last_space > start + self.chunk_size // 2:
                    end = last_space

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "text": chunk_text,
                        "source_file": source_file,
                        "chunk_index": chunk_index,
                    }
                )
                chunk_index += 1

            # Move start with overlap
            start = end - self.chunk_overlap
            if start < 0:
                start = end

        return chunks

    def process_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a single Markdown file.

        Args:
            file_path: Path to the Markdown file

        Returns:
            List of chunk dictionaries with text and metadata
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        filename = os.path.basename(file_path)
        return self._split_into_chunks(content, filename)

    def process_directory(self, dir_path: str) -> List[Dict[str, Any]]:
        """
        Process all Markdown files in a directory.

        Args:
            dir_path: Path to directory containing Markdown files

        Returns:
            List of all chunks from all files
        """
        all_chunks = []

        for filename in os.listdir(dir_path):
            if filename.endswith(".md"):
                file_path = os.path.join(dir_path, filename)
                chunks = self.process_file(file_path)
                all_chunks.extend(chunks)

        return all_chunks

    def process_uploaded_content(
        self, content: str, filename: str
    ) -> List[Dict[str, Any]]:
        """
        Process uploaded file content directly.

        Args:
            content: File content as string
            filename: Original filename

        Returns:
            List of chunk dictionaries
        """
        return self._split_into_chunks(content, filename)

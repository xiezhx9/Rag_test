"""
Document Manager - Track and manage indexed documents
"""

import os
import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

from .vector_store import VectorStore

load_dotenv()


class DocumentManager:
    """Manage document metadata and indexing status."""

    def __init__(self, metadata_file: str = None):
        self.metadata_file = metadata_file or "./document_metadata.json"
        self.vector_store = VectorStore()
        self._metadata = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from file."""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"documents": {}}

    def _save_metadata(self) -> None:
        """Save metadata to file."""
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self._metadata, f, ensure_ascii=False, indent=2)

    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all indexed documents.

        Returns:
            List of document info dicts
        """
        documents = []
        for doc_id, info in self._metadata.get("documents", {}).items():
            documents.append(
                {
                    "id": doc_id,
                    "filename": info.get("filename", "未知"),
                    "indexed_at": info.get("indexed_at", ""),
                    "chunk_count": info.get("chunk_count", 0),
                    "status": info.get("status", "indexed"),
                }
            )

        # Sort by indexed_at descending
        documents.sort(key=lambda x: x["indexed_at"], reverse=True)
        return documents

    def add_document(self, filename: str, chunk_count: int) -> str:
        """
        Register a newly indexed document.

        Args:
            filename: Original filename
            chunk_count: Number of chunks created

        Returns:
            Document ID
        """
        doc_id = str(uuid.uuid4())[:8]

        self._metadata["documents"][doc_id] = {
            "filename": filename,
            "indexed_at": datetime.now().isoformat(),
            "chunk_count": chunk_count,
            "status": "indexed",
        }

        self._save_metadata()
        return doc_id

    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from index.

        Args:
            doc_id: Document ID to delete

        Returns:
            True if deleted, False if not found
        """
        if doc_id not in self._metadata.get("documents", {}):
            return False

        filename = self._metadata["documents"][doc_id].get("filename")

        # Remove from metadata
        del self._metadata["documents"][doc_id]
        self._save_metadata()

        # Note: Actual vector deletion would require tracking chunk IDs
        # For simplicity, we just remove from metadata

        return True

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get document info by ID."""
        return self._metadata.get("documents", {}).get(doc_id)

    def get_total_chunks(self) -> int:
        """Get total number of chunks across all documents."""
        return sum(
            doc.get("chunk_count", 0)
            for doc in self._metadata.get("documents", {}).values()
        )

    def clear_all(self) -> None:
        """Clear all documents and metadata."""
        self._metadata = {"documents": {}}
        self._save_metadata()
        self.vector_store.delete_all()

"""
Vector Store - ChromaDB with persistent storage
"""

import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()


class VectorStore:
    """ChromaDB vector store wrapper."""

    def __init__(self, persist_dir: Optional[str] = None):
        self.persist_dir = persist_dir or os.environ.get(
            "CHROMA_PERSIST_DIR", "./chroma_db"
        )

        self.client = chromadb.PersistentClient(path=self.persist_dir)

        # Import embedding model to create embedding function
        from .embeddings import EmbeddingModel

        embedding_model = EmbeddingModel()

        # Create custom embedding function
        class CustomEmbeddingFunction:
            def name(self):
                return "custom_embedding_function"

            def __call__(self, input):
                # ChromaDB passes 'input' as a list of texts
                return embedding_model.embed_texts(input)

        embedding_function = CustomEmbeddingFunction()

        # Create or get collection with embedding function
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
            embedding_function=embedding_function,
        )

        self.client = chromadb.PersistentClient(path=self.persist_dir)

        # Import embedding model to create embedding function
        from .embeddings import EmbeddingModel

        embedding_model = EmbeddingModel()

        # Create custom embedding function
        class CustomEmbeddingFunction:
            def name(self):
                return "custom_embedding_function"

            def __call__(self, texts: List[str]):
                return embedding_model.embed_texts(texts)

        embedding_function = CustomEmbeddingFunction()

        # Create or get collection with embedding function
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
            embedding_function=embedding_function,
        )

        self.client = chromadb.PersistentClient(path=self.persist_dir)

        # Import embedding model to create embedding function
        from .embeddings import EmbeddingModel

        embedding_model = EmbeddingModel()

        # Create custom embedding function
        class CustomEmbeddingFunction:
            def __call__(self, texts: List[str]):
                return embedding_model.embed_texts(texts)

        embedding_function = CustomEmbeddingFunction()

        # Create or get collection with embedding function
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
            embedding_function=embedding_function,
        )

    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
        embeddings: Optional[List[List[float]]] = None,
    ) -> None:
        """
        Add documents to the vector store.

        Args:
            texts: List of document texts
            metadatas: Optional list of metadata dicts
            ids: Optional list of document IDs
            embeddings: Optional list of pre-computed embedding vectors
        """
        if not texts:
            return

        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]

        if metadatas is None:
            metadatas = [{} for _ in texts]

        # Add documents with embeddings if provided
        if embeddings is not None:
            self.collection.add(
                documents=texts, metadatas=metadatas, ids=ids, embeddings=embeddings
            )
        else:
            self.collection.add(documents=texts, metadatas=metadatas, ids=ids)

    def search(
        self,
        query_embedding: List[float],
        k: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.

        Args:
            query_embedding: Query vector
            k: Number of results to return
            where: Optional metadata filter

        Returns:
            List of results with id, text, metadata, and distance
        """
        if self.collection.count() == 0:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, self.collection.count()),
            where=where,
        )

        # Format results
        formatted = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                formatted.append(
                    {
                        "id": doc_id,
                        "text": results["documents"][0][i]
                        if results["documents"]
                        else "",
                        "metadata": results["metadatas"][0][i]
                        if results["metadatas"]
                        else {},
                        "distance": results["distances"][0][i]
                        if results["distances"]
                        else 0.0,
                    }
                )

        return formatted

    def delete_by_ids(self, ids: List[str]) -> None:
        """Delete documents by IDs."""
        if ids:
            self.collection.delete(ids=ids)

    def delete_all(self) -> None:
        """Delete all documents in the collection."""
        # Get all IDs and delete
        all_items = self.collection.get()
        if all_items["ids"]:
            self.collection.delete(ids=all_items["ids"])

    def get_document_count(self) -> int:
        """Return number of documents in the store."""
        return self.collection.count()

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents with their metadata."""
        results = self.collection.get()

        formatted = []
        if results["ids"]:
            for i, doc_id in enumerate(results["ids"]):
                formatted.append(
                    {
                        "id": doc_id,
                        "text": results["documents"][i] if results["documents"] else "",
                        "metadata": results["metadatas"][i]
                        if results["metadatas"]
                        else {},
                    }
                )

        return formatted

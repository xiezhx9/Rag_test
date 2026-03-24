"""
RAG Engine - Retrieval-Augmented Generation pipeline
"""

import os
import uuid
from typing import List, Dict, Any, Generator, Optional, Union
from dotenv import load_dotenv

from .llm_client import LLMClient
from .embeddings import EmbeddingModel
from .vector_store import VectorStore
from .document_processor import DocumentProcessor

load_dotenv()


class RAGEngine:
    """RAG pipeline engine."""

    def __init__(self):
        self.llm = LLMClient()
        self.embeddings = EmbeddingModel()
        self.vector_store = VectorStore()
        self.doc_processor = DocumentProcessor()
        self.top_k = int(os.environ.get("TOP_K", "5"))

    def index_documents(self, file_contents: Dict[str, Union[str, bytes]]) -> int:
        """
        Index documents from file contents.

        Args:
            file_contents: Dict mapping filename to content (str for text, bytes for binary)

        Returns:
            Number of chunks indexed
        """
        all_chunks = []
        all_texts = []
        all_metadatas = []
        all_ids = []

        for filename, content in file_contents.items():
            # Use process_uploaded_file for automatic format detection
            chunks = self.doc_processor.process_uploaded_file(content, filename)

            for chunk in chunks:
                chunk_id = str(uuid.uuid4())
                all_texts.append(chunk["text"])
                all_metadatas.append(
                    {
                        "source_file": chunk["source_file"],
                        "chunk_index": chunk["chunk_index"],
                    }
                )
                all_ids.append(chunk_id)

        if not all_texts:
            return 0

        # Generate embeddings
        embeddings = self.embeddings.embed_texts(all_texts)

        # Store in vector database
        self.vector_store.add_documents(
            texts=all_texts, metadatas=all_metadatas, ids=all_ids, embeddings=embeddings
        )

        return len(all_texts)

    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG system.

        Args:
            question: User question

        Returns:
            Dict with answer and sources
        """
        # Embed the question
        query_embedding = self.embeddings.embed_query(question)

        # Retrieve relevant documents
        results = self.vector_store.search(query_embedding, k=self.top_k)

        if not results:
            return {
                "answer": "抱歉，我没有找到相关的文档内容。请先上传一些文档。",
                "sources": [],
            }

        # Build context from retrieved documents
        context_parts = []
        sources = []
        seen_files = set()

        for result in results:
            context_parts.append(result["text"])
            source_file = result["metadata"].get("source_file", "未知")
            if source_file not in seen_files:
                sources.append(source_file)
                seen_files.add(source_file)

        context = "\n\n---\n\n".join(context_parts)

        # Build prompt
        system_prompt = """你是一个有帮助的助手，根据提供的文档内容回答问题。
请仅基于提供的文档内容回答，如果文档中没有相关信息，请如实说明。
回答要简洁明了，使用中文。"""

        user_message = f"""根据以下文档内容回答问题：

文档内容：
{context}

问题：{question}

请基于文档内容回答："""

        # Get answer from LLM
        answer = self.llm.chat(
            messages=[{"role": "user", "content": user_message}],
            system_prompt=system_prompt,
        )

        return {"answer": answer, "sources": sources}

    def stream_query(self, question: str) -> Generator[str, None, None]:
        """
        Stream query response for UI.

        Args:
            question: User question

        Yields:
            Response chunks
        """
        # Embed the question
        query_embedding = self.embeddings.embed_query(question)

        # Retrieve relevant documents
        results = self.vector_store.search(query_embedding, k=self.top_k)

        if not results:
            yield "抱歉，我没有找到相关的文档内容。请先上传一些文档。"
            return

        # Build context
        context_parts = []
        for result in results:
            context_parts.append(result["text"])

        context = "\n\n---\n\n".join(context_parts)

        # Build prompt
        system_prompt = """你是一个有帮助的助手，根据提供的文档内容回答问题。
请仅基于提供的文档内容回答，如果文档中没有相关信息，请如实说明。
回答要简洁明了，使用中文。"""

        user_message = f"""根据以下文档内容回答问题：

文档内容：
{context}

问题：{question}

请基于文档内容回答："""

        # Stream answer
        for chunk in self.llm.stream_chat(
            messages=[{"role": "user", "content": user_message}],
            system_prompt=system_prompt,
        ):
            yield chunk

    def get_sources(self, question: str) -> List[str]:
        """Get source files for a question."""
        query_embedding = self.embeddings.embed_query(question)
        results = self.vector_store.search(query_embedding, k=self.top_k)

        sources = []
        seen = set()
        for result in results:
            source_file = result["metadata"].get("source_file", "未知")
            if source_file not in seen:
                sources.append(source_file)
                seen.add(source_file)

        return sources

    def clear_index(self) -> None:
        """Clear all indexed documents."""
        self.vector_store.delete_all()

    def get_document_count(self) -> int:
        """Get number of indexed document chunks."""
        return self.vector_store.get_document_count()

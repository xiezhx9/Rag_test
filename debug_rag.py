#!/usr/bin/env python3
"""
RAG System Debugging Script
Run this to diagnose common issues
"""

import os
import sys
import httpx
import sqlite3
import chromadb
from dotenv import load_dotenv

load_dotenv()


def print_section(title):
    """Print a section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def test_embedding_model():
    """Test embedding model configuration and API."""
    print_section("1. Testing Embedding Model")

    try:
        from src.embeddings import EmbeddingModel

        print(f"Model name: {os.environ.get('EMBEDDING_MODEL', 'Not set')}")
        print(f"API base: {os.environ.get('EMBEDDING_API_BASE', 'Not set')}")

        embedding = EmbeddingModel()
        print(f"✓ Model loaded: {embedding.model_name}")
        print(f"✓ Dimension: {embedding.dimension}")

        # Test API
        test_text = "测试"
        embedding_vector = embedding.embed_query(test_text)
        print(f"✓ API test: {len(embedding_vector)}-dim vector generated")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_llm_client():
    """Test LLM client configuration and API."""
    print_section("2. Testing LLM Client")

    try:
        from src.llm_client import LLMClient

        print(f"Model: {os.environ.get('LLM_MODEL', 'Not set')}")
        print(f"API base: {os.environ.get('LLM_API_BASE', 'Not set')}")

        llm = LLMClient()
        print(f"✓ Model loaded: {llm.config['model']}")

        # Test API
        response = llm.chat(messages=[{"role": "user", "content": "你好"}])
        print(f"✓ API test: Response received ({len(response)} chars)")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_vector_store():
    """Test vector store and ChromaDB."""
    print_section("3. Testing Vector Store")

    try:
        from src.vector_store import VectorStore

        vector_store = VectorStore()
        print(f"✓ Vector store created")
        print(f"✓ Collection: {vector_store.collection.name}")
        print(f"✓ Document count: {vector_store.get_document_count()}")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_chroma_db():
    """Test ChromaDB directly."""
    print_section("4. Testing ChromaDB")

    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collections = client.list_collections()

        print(f"✓ ChromaDB connected")
        print(f"✓ Total collections: {len(collections)}")

        for collection in collections:
            print(f"\n  Collection: {collection.name}")
            print(f"    Documents: {collection.count()}")

            # Check dimension from SQLite
            conn = sqlite3.connect("./chroma_db/chroma.sqlite3")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT dimension FROM collections WHERE name=?", (collection.name,)
            )
            result = cursor.fetchone()
            if result:
                print(f"    Dimension (from DB): {result[0]}")
            conn.close()

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_api_connectivity():
    """Test API connectivity directly."""
    print_section("5. Testing API Connectivity")

    embedding_api = os.environ.get("EMBEDDING_API_BASE", "")
    embedding_key = os.environ.get("EMBEDDING_API_KEY", "")
    llm_api = os.environ.get("LLM_API_BASE", "")

    # Test Embedding API
    print("Testing Embedding API...")
    try:
        response = httpx.post(
            f"{embedding_api}/embeddings",
            headers={"Authorization": f"Bearer {embedding_key}"},
            json={"model": "xop3qwen8bembedding", "input": "测试"},
            timeout=10,
        )
        if response.status_code == 200:
            data = response.json()
            dim = len(data["data"][0]["embedding"])
            print(f"✓ Embedding API: {dim}-dim vector")
        else:
            print(f"✗ Embedding API: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"✗ Embedding API: {e}")

    # Test LLM API
    print("\nTesting LLM API...")
    try:
        response = httpx.post(
            f"{llm_api}/chat/completions",
            headers={"Authorization": f"Bearer {embedding_key}"},
            json={
                "model": "xop35qwen2b",
                "messages": [{"role": "user", "content": "你好"}],
            },
            timeout=10,
        )
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            print(f"✓ LLM API: Response received ({len(content)} chars)")
        else:
            print(f"✗ LLM API: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"✗ LLM API: {e}")


def test_rag_engine():
    """Test RAG engine integration."""
    print_section("6. Testing RAG Engine")

    try:
        from src.rag_engine import RAGEngine

        engine = RAGEngine()
        print(f"✓ RAG Engine initialized")
        print(f"  - LLM: {engine.llm.config['model']}")
        print(f"  - Embedding: {engine.embeddings.model_name}")
        print(f"  - Embedding Dimension: {engine.embeddings.dimension}")
        print(f"  - Document Count: {engine.get_document_count()}")

        # Test query
        print("\nTesting query...")
        try:
            results = engine.query("测试问题")
            print(f"✓ Query successful")
            print(f"  - Answer: {results['answer'][:100]}...")
            print(f"  - Sources: {len(results['sources'])}")
        except Exception as e:
            print(f"✗ Query failed: {e}")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  RAG SYSTEM DEBUGGING TOOL")
    print("=" * 60)

    results = {
        "Embedding Model": test_embedding_model(),
        "LLM Client": test_llm_client(),
        "Vector Store": test_vector_store(),
        "ChromaDB": test_chroma_db(),
        "API Connectivity": test_api_connectivity(),
        "RAG Engine": test_rag_engine(),
    }

    # Summary
    print_section("SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")

    print(f"\n  Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n  ✓ All tests passed! System is working correctly.")
        return 0
    else:
        print(f"\n  ✗ {total - passed} test(s) failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

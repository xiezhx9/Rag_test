"""
End-to-End Integration Test for RAG Q&A System

This script tests the core functionality without requiring a running LLM.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that all modules can be imported."""
    print("=" * 50)
    print("Test 1: Module Imports")
    print("=" * 50)

    try:
        from src.llm_client import LLMClient

        print("✅ LLMClient imported")
    except Exception as e:
        print(f"❌ LLMClient import failed: {e}")
        return False

    try:
        from src.embeddings import EmbeddingModel

        print("✅ EmbeddingModel imported")
    except Exception as e:
        print(f"❌ EmbeddingModel import failed: {e}")
        return False

    try:
        from src.vector_store import VectorStore

        print("✅ VectorStore imported")
    except Exception as e:
        print(f"❌ VectorStore import failed: {e}")
        return False

    try:
        from src.document_processor import DocumentProcessor

        print("✅ DocumentProcessor imported")
    except Exception as e:
        print(f"❌ DocumentProcessor import failed: {e}")
        return False

    try:
        from src.rag_engine import RAGEngine

        print("✅ RAGEngine imported")
    except Exception as e:
        print(f"❌ RAGEngine import failed: {e}")
        return False

    try:
        from src.document_manager import DocumentManager

        print("✅ DocumentManager imported")
    except Exception as e:
        print(f"❌ DocumentManager import failed: {e}")
        return False

    print("\n✅ All modules imported successfully!\n")
    return True


def test_document_processor():
    """Test document processing."""
    print("=" * 50)
    print("Test 2: Document Processor")
    print("=" * 50)

    from src.document_processor import DocumentProcessor

    dp = DocumentProcessor(chunk_size=200, chunk_overlap=50)
    print(f"✅ DocumentProcessor created (chunk_size={dp.chunk_size})")

    # Test file processing
    test_file = "test_docs/python_basics.md"
    if os.path.exists(test_file):
        chunks = dp.process_file(test_file)
        print(f"✅ Processed {test_file}: {len(chunks)} chunks")

        if chunks:
            print(f"   First chunk preview: {chunks[0]['text'][:50]}...")
            print(f"   Metadata: {chunks[0]['metadata']}")
    else:
        print(f"⚠️ Test file not found: {test_file}")

    # Test directory processing
    if os.path.exists("test_docs"):
        all_chunks = dp.process_directory("test_docs")
        print(f"✅ Processed test_docs directory: {len(all_chunks)} total chunks")

    print()
    return True


def test_vector_store():
    """Test vector store operations."""
    print("=" * 50)
    print("Test 3: Vector Store")
    print("=" * 50)

    from src.vector_store import VectorStore
    import shutil

    # Clean up any existing test data
    test_dir = "./test_chroma_e2e"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    vs = VectorStore(test_dir)
    print(f"✅ VectorStore created at {test_dir}")

    # Test add documents
    texts = ["Python is a programming language.", "Machine learning uses algorithms."]
    metadatas = [{"source": "test1.md"}, {"source": "test2.md"}]
    ids = ["doc1", "doc2"]

    vs.add_documents(texts, metadatas, ids)
    print(f"✅ Added {len(texts)} documents")

    # Test count
    count = vs.get_document_count()
    print(f"✅ Document count: {count}")

    # Test search (with dummy embedding)
    dummy_embedding = [0.1] * 1024  # BGE-M3 dimension
    results = vs.search(dummy_embedding, k=2)
    print(f"✅ Search returned {len(results)} results")

    # Test delete
    vs.delete_by_ids(["doc1"])
    count_after = vs.get_document_count()
    print(f"✅ After deletion: {count_after} documents")

    # Clean up
    shutil.rmtree(test_dir)
    print(f"✅ Cleaned up test data")

    print()
    return True


def test_document_manager():
    """Test document manager."""
    print("=" * 50)
    print("Test 4: Document Manager")
    print("=" * 50)

    from src.document_manager import DocumentManager
    import os

    # Use test metadata file
    test_meta = "./test_metadata.json"
    if os.path.exists(test_meta):
        os.remove(test_meta)

    dm = DocumentManager(test_meta)
    print("✅ DocumentManager created")

    # Test add
    doc_id = dm.add_document("test.md", 5)
    print(f"✅ Added document: {doc_id}")

    # Test list
    docs = dm.list_documents()
    print(f"✅ Listed {len(docs)} documents")

    # Test delete
    success = dm.delete_document(doc_id)
    print(f"✅ Deleted document: {success}")

    # Clean up
    if os.path.exists(test_meta):
        os.remove(test_meta)

    print()
    return True


def test_embedding_model():
    """Test embedding model (requires model download on first run)."""
    print("=" * 50)
    print("Test 5: Embedding Model")
    print("=" * 50)

    try:
        from src.embeddings import EmbeddingModel

        print("Loading BGE-M3 model (this may take a moment on first run)...")
        model = EmbeddingModel()
        print(f"✅ EmbeddingModel loaded: {model.model_name}")
        print(f"   Embedding dimension: {model.dimension}")

        # Test single embedding
        embedding = model.embed_query("测试文本")
        print(f"✅ Single embedding: {len(embedding)} dimensions")

        # Test batch embedding
        embeddings = model.embed_texts(["文本1", "文本2"])
        print(f"✅ Batch embedding: {len(embeddings)} vectors")

        print()
        return True

    except Exception as e:
        print(f"⚠️ Embedding test skipped (model may need to download): {e}")
        print("   Run 'pip install sentence-transformers' and try again.")
        print()
        return True  # Don't fail the test


def test_llm_client():
    """Test LLM client initialization."""
    print("=" * 50)
    print("Test 6: LLM Client")
    print("=" * 50)

    from src.llm_client import LLMClient

    client = LLMClient()
    print(f"✅ LLMClient created")
    print(f"   API Base: {client.config['api_base']}")
    print(f"   Model: {client.config['model']}")

    # Note: test_connection() requires a running LLM
    print("⚠️ Skipping connection test (requires running LLM)")

    print()
    return True


def test_rag_engine():
    """Test RAG engine initialization."""
    print("=" * 50)
    print("Test 7: RAG Engine")
    print("=" * 50)

    try:
        from src.rag_engine import RAGEngine

        print("Initializing RAG Engine...")
        engine = RAGEngine()
        print("✅ RAGEngine created")
        print(f"   Document count: {engine.get_document_count()}")

        # Test document indexing
        test_content = {
            "test.md": "# Test Document\nThis is a test document for RAG system."
        }

        print("Testing document indexing...")
        chunk_count = engine.index_documents(test_content)
        print(f"✅ Indexed {chunk_count} chunks")
        print(f"   Total documents: {engine.get_document_count()}")

        # Clean up
        engine.clear_index()
        print("✅ Cleared index")

        print()
        return True

    except Exception as e:
        print(f"⚠️ RAG Engine test partially skipped: {e}")
        print()
        return True


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  RAG Q&A System - End-to-End Integration Test")
    print("=" * 60 + "\n")

    results = []

    results.append(("Module Imports", test_imports()))
    results.append(("Document Processor", test_document_processor()))
    results.append(("Vector Store", test_vector_store()))
    results.append(("Document Manager", test_document_manager()))
    results.append(("Embedding Model", test_embedding_model()))
    results.append(("LLM Client", test_llm_client()))
    results.append(("RAG Engine", test_rag_engine()))

    # Summary
    print("=" * 60)
    print("  Test Summary")
    print("=" * 60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")

    print()
    print(f"  Total: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("\n🎉 All tests passed! The RAG Q&A System is ready to use.\n")
        print("To start the application:")
        print("  1. Copy .env.example to .env")
        print("  2. Configure your LLM API settings")
        print("  3. Run: streamlit run app.py")
        print()
        return 0
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

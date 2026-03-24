"""
RAG Q&A System - Main Application
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="RAG Q&A System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Main content
st.markdown('<p class="main-header">📚 RAG Q&A System</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">基于您的文档进行智能问答</p>', unsafe_allow_html=True
)

# Quick stats
from src.rag_engine import RAGEngine
from src.document_manager import DocumentManager


@st.cache_resource
def get_rag_engine():
    return RAGEngine()


@st.cache_resource
def get_doc_manager():
    return DocumentManager()


try:
    engine = get_rag_engine()
    doc_manager = get_doc_manager()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📄 文档数量", len(doc_manager.list_documents()))

    with col2:
        st.metric("📝 文本块数量", engine.get_document_count())

    with col3:
        st.metric("🤖 向量维度", engine.embeddings.dimension)

    st.markdown("---")

    # Quick actions
    st.subheader("🚀 快速开始")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **1. 上传文档**
        
        前往 📄 Documents 页面上传您的 Markdown 文档。
        系统会自动处理并向量化文档内容。
        """)

    with col2:
        st.markdown("""
        **2. 开始问答**
        
        前往 💬 Chat 页面开始提问。
        系统会基于您的文档内容给出答案。
        """)

    st.markdown("---")

    # System status
    st.subheader("⚙️ 系统状态")

    llm_client = engine.llm
    config = llm_client.config

    st.json(
        {
            "LLM API": config["api_base"],
            "Model": config["model"],
            "Embedding Model": engine.embeddings.model_name,
        }
    )

except Exception as e:
    st.error(f"初始化失败: {str(e)}")
    st.info("请检查 .env 配置文件是否正确设置。")

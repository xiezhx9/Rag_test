"""
Documents Page - Upload and manage documents
"""

import streamlit as st
import time
import os
from datetime import datetime

st.set_page_config(
    page_title="文档管理 - RAG Q&A System", page_icon="📄", layout="wide"
)

from src.rag_engine import RAGEngine
from src.document_manager import DocumentManager


@st.cache_resource
def get_rag_engine():
    return RAGEngine()


@st.cache_resource
def get_doc_manager():
    return DocumentManager()


engine = get_rag_engine()
doc_manager = get_doc_manager()

# Page header
st.title("📄 文档管理")
st.markdown("上传和管理您的文档（支持 Markdown、PDF、Word、PPT）")

st.markdown("---")

# Upload section
st.subheader("📤 上传文档")

# Tab for file upload and text paste
tab1, tab2 = st.tabs(["📁 文件上传", "📝 文本粘贴"])

with tab1:
    uploaded_files = st.file_uploader(
        "选择文档文件",
        type=["md", "pdf", "docx", "pptx"],
        accept_multiple_files=True,
        help="支持 .md、.pdf、.docx、.pptx 格式，可拖拽上传多个文件",
    )

    if uploaded_files:
        if st.button("🚀 开始处理", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            file_contents = {}

            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"正在处理: {uploaded_file.name}")

                # Read file content
                content = uploaded_file.read()

                # Get file extension
                ext = os.path.splitext(uploaded_file.name.lower())[1]

                # For text files (md), decode to string; for binary files, keep as bytes
                if ext in [".md", ".txt"]:
                    file_contents[uploaded_file.name] = content.decode("utf-8")
                else:
                    file_contents[uploaded_file.name] = content

                progress_bar.progress((i + 1) / len(uploaded_files) * 0.5)

            # Index documents
            status_text.text("正在向量化...")
            chunk_count = engine.index_documents(file_contents)
            progress_bar.progress(0.8)

            # Update metadata
            for filename in file_contents.keys():
                doc_manager.add_document(filename, chunk_count // len(file_contents))

            progress_bar.progress(1.0)
            status_text.text("完成!")

            st.success(
                f"✅ 成功处理 {len(uploaded_files)} 个文件，共 {chunk_count} 个文本块"
            )

            # Clear cache to refresh
            time.sleep(1)
            st.rerun()

with tab2:
    st.markdown("""
    **直接粘贴文本内容**

    将您的 Markdown 文本直接粘贴到下方，系统会自动创建文档并处理。
    """)

    text_input = st.text_area(
        "粘贴 Markdown 内容",
        height=300,
        placeholder="# 在这里粘贴您的文档内容...",
        help="支持 Markdown 格式，系统会自动解析和向量化",
    )

    if st.button("🚀 处理粘贴的文本", type="primary"):
        if not text_input.strip():
            st.warning("请输入文本内容")
        else:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pasted_text_{timestamp}.md"

            # Process text
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text(f"正在处理: {filename}")
            file_contents = {filename: text_input}

            # Index documents
            status_text.text("正在向量化...")
            chunk_count = engine.index_documents(file_contents)
            progress_bar.progress(0.8)

            # Update metadata
            doc_manager.add_document(filename, chunk_count)

            progress_bar.progress(1.0)
            status_text.text("完成!")

            st.success(f"✅ 成功处理文本，共 {chunk_count} 个文本块")

            # Clear cache to refresh
            time.sleep(1)
            st.rerun()

st.markdown("---")

# Document list section
st.subheader("📚 已索引文档")

documents = doc_manager.list_documents()

if not documents:
    st.info("暂无文档。请上传 Markdown、PDF、Word 或 PPT 文件开始使用。")
else:
    # Display documents in a table
    for doc in documents:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

            with col1:
                st.markdown(f"**📄 {doc['filename']}**")

            with col2:
                st.text(f"{doc['chunk_count']} 个文本块")

            with col3:
                try:
                    indexed_time = datetime.fromisoformat(doc["indexed_at"])
                    st.text(indexed_time.strftime("%Y-%m-%d %H:%M"))
                except:
                    st.text(doc["indexed_at"][:16] if doc["indexed_at"] else "未知")

            with col4:
                if st.button("🗑️", key=f"del_{doc['id']}", help="删除文档"):
                    doc_manager.delete_document(doc["id"])
                    st.success(f"已删除: {doc['filename']}")
                    time.sleep(0.5)
                    st.rerun()

            st.markdown("---")

# Clear all section
st.markdown("---")
st.subheader("⚠️ 危险操作")

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("清除所有文档和索引数据。此操作不可恢复。")

with col2:
    if st.button("🗑️ 清除所有", type="secondary"):
        if st.session_state.get("confirm_clear"):
            engine.clear_index()
            doc_manager.clear_all()
            st.session_state["confirm_clear"] = False
            st.success("已清除所有数据")
            time.sleep(1)
            st.rerun()
        else:
            st.session_state["confirm_clear"] = True
            st.warning("再次点击确认清除")

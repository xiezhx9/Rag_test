"""
Chat Page - Q&A interface
"""

import streamlit as st
from typing import List, Dict

st.set_page_config(
    page_title="智能问答 - RAG Q&A System", page_icon="💬", layout="wide"
)

from src.rag_engine import RAGEngine


@st.cache_resource
def get_rag_engine():
    return RAGEngine()


engine = get_rag_engine()

# Page header
st.title("💬 智能问答")
st.markdown("基于您的文档内容进行问答")

st.markdown("---")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for chat history
with st.sidebar:
    st.subheader("📜 对话历史")

    if st.button("🗑️ 清空对话", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")

    # Show recent questions
    if st.session_state.chat_history:
        for i, msg in enumerate(reversed(st.session_state.chat_history[-10:])):
            if msg["role"] == "user":
                st.markdown(f"**Q:** {msg['content'][:50]}...")
    else:
        st.info("暂无对话记录")

# Main chat area
st.subheader("🤔 提问")

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        # Show sources for assistant messages
        if msg["role"] == "assistant" and "sources" in msg:
            if msg["sources"]:
                st.markdown("---")
                st.markdown("**📚 参考来源:**")
                for source in msg["sources"]:
                    st.markdown(f"- {source}")

# Chat input
if prompt := st.chat_input("输入您的问题..."):
    # Check if documents are indexed
    if engine.get_document_count() == 0:
        st.warning("⚠️ 请先上传文档！前往 📄 Documents 页面上传您的 Markdown 文件。")
    else:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            # Stream response
            for chunk in engine.stream_query(prompt):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

            # Get sources
            sources = engine.get_sources(prompt)

            if sources:
                st.markdown("---")
                st.markdown("**📚 参考来源:**")
                for source in sources:
                    st.markdown(f"- {source}")

            # Save to history
            st.session_state.chat_history.append(
                {"role": "assistant", "content": full_response, "sources": sources}
            )

# Quick questions
st.markdown("---")
st.subheader("💡 快捷问题")

quick_questions = ["这些文档主要讲了什么？", "总结一下主要内容", "有哪些重要的概念？"]

cols = st.columns(len(quick_questions))
for i, question in enumerate(quick_questions):
    with cols[i]:
        if st.button(question, key=f"quick_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": question})
            st.rerun()

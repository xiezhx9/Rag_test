# RAG Q&A System

基于 Streamlit、Chroma 和 BGE-M3 的轻量级 RAG 问答系统。

## 功能

- 📄 Markdown 文档上传与管理
- 🔍 自动向量化入库
- 💬 流式问答界面
- 📚 来源引用显示
- 🐳 Docker 一键部署

## 快速开始

```bash
# 安装依赖
uv sync

# 配置环境
cp .env.example .env

# 启动应用
uv run streamlit run app.py
```

## 技术栈

- **前端**: Streamlit
- **向量数据库**: Chroma
- **Embedding**: BGE-M3
- **LLM**: OpenAI 兼容 API

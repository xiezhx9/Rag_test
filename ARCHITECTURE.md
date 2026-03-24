# RAG QA System - 项目架构说明文档

## 目录
1. [项目概述](#项目概述)
2. [项目结构](#项目结构)
3. [使用方法](#使用方法)
4. [代码结构说明](#代码结构说明)
5. [技术选型说明](#技术选型说明)
6. [RAG 流程详解](#rag-流程详解)
7. [部署与运维](#部署与运维)

---

## 项目概述

这是一个基于 **Retrieval-Augmented Generation (RAG)** 技术的问答系统，专为个人博客文档设计。系统支持多种文档格式（Markdown、PDF、Word、PowerPoint），通过向量数据库和 LLM 实现智能问答。

### 核心特性
- ✅ 多格式文档支持（MD、PDF、DOCX、PPTX）
- ✅ 智能文本分块与重叠处理
- ✅ 流式响应生成
- ✅ 来源引用与追溯
- ✅ 持久化向量数据库
- ✅ Docker 容器化部署
- ✅ 完整的测试与调试工具

---

## 项目结构

```
rag-qa-system/
├── src/                          # 核心源代码模块
│   ├── __init__.py
│   ├── rag_engine.py             # RAG 流程编排层
│   ├── document_manager.py       # 文档元数据管理
│   ├── document_processor.py     # 多格式文档处理
│   ├── embeddings.py             # 嵌入模型封装
│   ├── llm_client.py             # LLM API 客户端
│   └── vector_store.py           # ChromaDB 向量存储封装
│
├── pages/                        # Streamlit UI 页面
│   ├── 1_Documents.py            # 文档上传与管理界面
│   └── 2_Chat.py                 # 问答交互界面
│
├── test_docs/                    # 测试文档目录
│   ├── ml_intro.md
│   ├── python_basics.md
│   ├── python_tutorial.md
│   └── rag_guide.md
│
├── chroma_db/                    # 向量数据库持久化存储
├── knowledge_base_docs/          # 知识库文档目录
├── app.py                        # Streamlit 主应用入口
├── debug_rag.py                  # 调试与诊断脚本
├── test_e2e.py                   # 端到端集成测试
│
├── requirements.txt              # Python 依赖
├── pyproject.toml                # 项目配置（uv 包管理器）
├── uv.lock                       # 依赖锁定文件
├── Dockerfile                    # Docker 容器配置
├── docker-compose.yml            # Docker 编排配置
├── .env.example                  # 环境变量模板
├── .dockerignore                 # Docker 忽略规则
└── document_metadata.json        # 已索引文档元数据
```

---

## 使用方法

### 1. 开发模式运行

```bash
# 安装依赖（使用 uv 包管理器）
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥

# 启动 Streamlit 应用
uv run streamlit run app.py
```

访问：http://localhost:8501

### 2. Docker 部署

```bash
# 构建并启动 Docker 容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

访问：http://localhost:8501

### 3. 调试模式

```bash
# 运行诊断脚本，测试所有组件
python debug_rag.py
```

### 4. 测试模式

```bash
# 运行端到端集成测试
python test_e2e.py
```

---

## 代码结构说明

### 核心架构模式

系统采用模块化架构，职责清晰分离：

#### 1. **rag_engine.py** - 流程编排层
- 协调整个 RAG 流程
- 提供同步查询和流式查询两种接口
- 管理文档索引和查询生命周期

**核心方法：**
- `index_documents()`: 索引文档
- `query()`: 同步查询
- `stream_query()`: 流式查询
- `get_sources()`: 获取查询来源

#### 2. **document_processor.py** - 文档处理层
- 多格式文档解析
- 智能文本分块
- 边界检测（句子/段落）

**支持的格式：**
- Markdown (.md)
- 文本 (.txt)
- PDF (.pdf) - PyPDF2
- Word (.docx) - python-docx
- PowerPoint (.pptx) - python-pptx

**分块策略：**
- 默认块大小：512 字符
- 默认重叠：50 字符
- 智能边界检测：优先在句子/段落边界分割

#### 3. **vector_store.py** - 数据存储层
- ChromaDB 向量数据库封装
- 持久化向量存储
- 元数据管理

**配置：**
- 数据库：ChromaDB (SQLite-based)
- 集合名称：`documents`
- 距离度量：余弦相似度
- 索引类型：HNSW (Hierarchical Navigable Small World)

#### 4. **embeddings.py** - 嵌入层
- 远程嵌入模型 API 封装
- 批量处理优化
- 自动维度检测

**配置：**
- API 端点：OpenAI-compatible
- 模型：xop3qwen8bembedding
- 向量维度：1024
- 批处理：50 条/批，200KB/批上限

#### 5. **llm_client.py** - LLM 集成层
- OpenAI-compatible API 客户端
- 流式聊天支持
- 消息管理

**配置：**
- API 端点：OpenAI-compatible
- 模型：xop35qwen2b (7B 参数)
- 流式响应：✅

#### 6. **document_manager.py** - 元数据层
- 已索引文档跟踪
- 元数据持久化
- 文档生命周期管理

**存储：**
- JSON 文件：`document_metadata.json`

### UI 层（Streamlit 页面）

#### **1_Documents.py** - 文档管理页面
- 文件上传（拖拽、多文件）
- 文本粘贴选项
- 上传进度条
- 文档列表（显示元数据）
- 单个文档删除
- 清空所有功能

#### **2_Chat.py** - 问答界面
- 流式聊天界面
- 来源引用显示
- 聊天历史侧边栏
- 快捷问题按钮
- 文档数量验证

#### **app.py** - 主应用
- 系统状态概览
- 快捷操作入口

---

## 技术选型说明

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Streamlit** | 最新版 | Web UI 框架 |
| **Python** | 3.10+ | 核心语言 |

**选择理由：**
- Streamlit 提供快速、简洁的 Python Web 应用开发
- 内置流式响应支持
- 适合数据科学和 AI 应用

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.10+ | 核心语言 |
| **uv** | 最新版 | 包管理器和依赖解析器 |
| **llama-index** | 最新版 | RAG 框架和工具 |
| **OpenAI SDK** | 最新版 | LLM 和嵌入 API 客户端 |

**选择理由：**
- `uv`：比 pip 快 10-100 倍的包管理器
- `llama-index`：成熟的 RAG 框架，丰富的工具链
- `OpenAI SDK`：统一接口，支持多种 LLM 提供商

### 数据存储

| 技术 | 版本 | 用途 |
|------|------|------|
| **ChromaDB** | 最新版 | 向量数据库 |
| **SQLite** | 内置 | ChromaDB 底层数据库 |

**选择理由：**
- ChromaDB：零配置、嵌入式、持久化
- 适合 50 个文档的小规模应用
- SQLite 无需额外服务，开箱即用

### 文档处理

| 技术 | 版本 | 用途 |
|------|------|------|
| **pypdf** | 最新版 | PDF 文本提取 |
| **python-docx** | 最新版 | Word 文档解析 |
| **python-pptx** | 最新版 | PowerPoint 解析 |

### 基础设施

| 技术 | 版本 | 用途 |
|------|------|------|
| **Docker** | 最新版 | 容器化 |
| **Docker Compose** | 最新版 | 多容器编排 |
| **uv** | 最新版 | Docker 中的依赖管理 |

---

## RAG 流程详解

### 完整数据流

```
用户上传文档
    ↓
格式检测与文本提取
    ↓
智能分块（512 字符/块，50 字符重叠）
    ↓
批量嵌入生成（50 条/批，200KB/批）
    ↓
向量存储（ChromaDB，余弦相似度）
    ↓
用户提问
    ↓
查询嵌入生成
    ↓
向量相似性搜索（TOP_K=5）
    ↓
上下文构建（去重、拼接）
    ↓
提示词工程（系统提示 + 用户提示）
    ↓
LLM 流式生成
    ↓
来源引用展示
```

### 阶段 1：文档索引流程

**文件：** `rag_engine.py::index_documents()`, `document_processor.py`, `vector_store.py`

```python
# 1. 文档上传（bytes/string）
document_bytes = uploaded_file.read()

# 2. 格式检测与文本提取
if file_extension == '.md':
    text = document_bytes.decode('utf-8')
elif file_extension == '.pdf':
    text = extract_pdf_text(document_bytes)
elif file_extension == '.docx':
    text = extract_word_text(document_bytes)
elif file_extension == '.pptx':
    text = extract_ppt_text(document_bytes)

# 3. 智能分块
chunks = document_processor.split_into_chunks(text, source_file)

# 4. 批量嵌入生成
embeddings = embeddings_api.embed_batch([chunk['text'] for chunk in chunks])

# 5. 向量存储
vector_store.add_documents(
    texts=[chunk['text'] for chunk in chunks],
    embeddings=embeddings,
    metadatas=[{'source_file': chunk['source_file'], 'chunk_index': chunk['chunk_index']} for chunk in chunks]
)
```

**分块算法：**
```python
def _split_into_chunks(text: str, source_file: str):
    # 智能边界检测
    last_period = text.rfind("。", start, end)
    last_newline = text.rfind("\n", start, end)
    last_space = text.rfind(" ", start, end)
    break_point = max(last_period, last_newline)

    # 创建重叠块
    chunk_text = text[start:end]
    chunks.append({
        "text": chunk_text,
        "source_file": source_file,
        "chunk_index": chunk_index
    })

    # 向前移动（保留重叠）
    start = end - self.chunk_overlap
```

### 阶段 2：查询处理流程

**文件：** `rag_engine.py::query()`, `vector_store.py::search()`

```python
# 1. 用户提问
question = "机器学习的基本概念是什么？"

# 2. 查询嵌入生成
query_embedding = embeddings_api.embed([question])[0]

# 3. 向量相似性搜索
results = vector_store.search(
    query_embedding,
    top_k=5,
    n_results=5
)

# 4. 上下文构建
context = "\n---\n".join([result['text'] for result in results])
sources = list(set([result['metadata']['source_file'] for result in results]))

# 5. 提示词工程
system_prompt = """你是一个有帮助的助手，根据提供的文档内容回答问题。
请仅基于提供的文档内容回答，如果文档中没有相关信息，请如实说明。
回答要简洁明了，使用中文。"""

user_prompt = f"""根据以下文档内容回答问题：
文档内容：
{context}

问题：{question}
请基于文档内容回答："""

# 6. LLM 生成
answer = llm_client.chat_completion(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)
```

**提示词模板：**
```
系统提示：
你是一个有帮助的助手，根据提供的文档内容回答问题。
请仅基于提供的文档内容回答，如果文档中没有相关信息，请如实说明。
回答要简洁明了，使用中文。

用户提示：
根据以下文档内容回答问题：
文档内容：
[检索到的上下文]

问题：{用户问题}
请基于文档内容回答：
```

### 阶段 3：流式响应

**文件：** `rag_engine.py::stream_query()`, `llm_client.py::stream_chat()`

```python
# 流式响应模式
for chunk in engine.stream_query(question):
    full_response += chunk
    response_placeholder.markdown(full_response + "▌")

# 移除光标
response_placeholder.markdown(full_response)

# 显示来源
st.markdown(f"**来源：** {', '.join(sources)}")
```

---

## 部署与运维

### Docker 配置

**docker-compose.yml：**
```yaml
version: '3.8'

services:
  rag-qa-system:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - chroma_data:/app/chroma_db
      - ./document_metadata.json:/app/document_metadata.json
      - ./knowledge_base_docs:/app/knowledge_base_docs
    environment:
      - LLM_API_BASE=http://host.docker.internal:11434/v1
      - LLM_API_KEY=not-needed
      - LLM_MODEL=qwen2.5:7b
      - EMBEDDING_API_BASE=http://host.docker.internal:11434/v1/embeddings
      - EMBEDDING_MODEL=nomic-embed-text
      - CHROMA_PERSIST_DIR=/app/chroma_db
      - CHUNK_SIZE=512
      - CHUNK_OVERLAP=50
      - TOP_K=5
    extra_hosts:
      - "host.docker.internal:host-gateway"

volumes:
  chroma_data:
```

**关键配置说明：**
- `host.docker.internal`：Docker 容器访问宿主机的桥梁
- `chroma_data`：Docker 卷，持久化向量数据库
- 环境变量：所有配置通过 `.env` 文件管理

### 环境变量配置

**.env 文件：**
```bash
# LLM 配置
LLM_API_BASE=https://maas-api.cn-huabei-1.xf-yun.com/v2
LLM_API_KEY=your_api_key_here
LLM_MODEL=xop35qwen2b

# 嵌入模型配置
EMBEDDING_API_BASE=https://maas-api.cn-huabei-1.xf-yun.com/v2/embeddings
EMBEDDING_MODEL=xop3qwen8bembedding

# 向量存储配置
CHROMA_PERSIST_DIR=./chroma_db

# 文档处理配置
CHUNK_SIZE=512
CHUNK_OVERLAP=50

# 检索配置
TOP_K=5
```

### 性能特征

**索引性能：**
- 批处理大小：50 条文本
- 每批最大字符数：200KB
- 预估：每批约 100 个块（512 字符/块）

**检索性能：**
- TOP_K：5 个块
- 距离度量：余弦相似度
- 索引类型：HNSW（层次化可导航小世界图）

**内存占用：**
- 向量维度：1024 个浮点数
- 每块约 4KB
- 100 个块 ≈ 400KB 向量存储

---

## 配置文件详解

### pyproject.toml

```toml
[project]
name = "rag-qa-system"
version = "0.1.0"
description = "RAG-based QA system for personal blog documents"
requires-python = ">=3.10"
dependencies = [
    "streamlit>=1.28.0",
    "llama-index>=0.10.0",
    "llama-index-llms-openai>=0.1.0",
    "chromadb>=0.4.0",
    "httpx>=0.25.0",
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
    "tqdm>=4.66.0",
    "pypdf>=3.17.0",
    "python-docx>=1.1.0",
    "python-pptx>=0.6.21",
]

[tool.uv]
dev-dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### requirements.txt

```
streamlit>=1.28.0
llama-index>=0.10.0
llama-index-llms-openai>=0.1.0
chromadb>=0.4.0
httpx>=0.25.0
openai>=1.0.0
python-dotenv>=1.0.0
tqdm>=4.66.0
pypdf>=3.17.0
python-docx>=1.1.0
python-pptx>=0.6.21
```

---

## 调试与测试

### debug_rag.py

运行诊断脚本测试所有组件：

```bash
python debug_rag.py
```

**测试项：**
1. ✅ 嵌入模型配置
2. ✅ LLM 客户端连接
3. ✅ 向量存储初始化
4. ✅ ChromaDB 直接访问
5. ✅ API 连接性
6. ✅ RAG 引擎集成

### test_e2e.py

端到端集成测试：

```bash
python test_e2e.py
```

---

## 关键设计决策

### 1. 为什么选择传统 RAG 而不是 GraphRAG？

**选择原因：**
- 博客内容实体关系稀疏，GraphRAG 需要昂贵的 LLM 实体提取
- 50 个文档规模，传统 RAG 足够高效
- GraphRAG 增加复杂度，维护成本高

### 2. 为什么选择 ChromaDB 而不是 Pinecone/FAISS？

**选择原因：**
- 嵌入式、零配置
- 完美适配 50 个文档的小规模应用
- SQLite 持久化，无需额外服务
- 开箱即用，降低运维复杂度

### 3. 为什么选择远程嵌入而不是本地嵌入？

**选择原因：**
- 更好的中文支持
- 混合检索能力
- API 灵活性，易于切换模型

### 4. 为什么使用 OpenAI-compatible API？

**选择原因：**
- 灵活集成本地 LLM（Ollama、vLLM 等）
- 统一的接口标准
- 易于迁移和扩展

### 5. 为什么使用流式响应？

**选择原因：**
- 更好的用户体验
- 实时反馈
- 降低感知延迟

### 6. 为什么使用智能分块？

**选择原因：**
- 保留上下文连续性（重叠）
- 在句子/段落边界分割
- 避免截断信息

### 7. 为什么使用元数据跟踪？

**选择原因：**
- 追踪已索引文档
- 统计块数量
- 支持文档生命周期管理

---

## 总结

这是一个**生产就绪**的 RAG 问答系统，专为个人博客文档设计。系统架构清晰、模块化、易于扩展，支持多种文档格式和流式响应。通过 Docker 容器化部署，可以快速启动和运行。

**系统特点：**
- ✅ 多格式文档支持
- ✅ 智能分块与重叠
- ✅ 流式响应
- ✅ 来源引用
- ✅ 持久化存储
- ✅ Docker 部署
- ✅ 完整测试工具

**适用场景：**
- 个人知识库问答
- 文档智能检索
- 学习资料问答
- 企业文档助手

**下一步：**
1. 配置 `.env` 文件
2. 运行 `uv sync` 安装依赖
3. 启动应用：`uv run streamlit run app.py`
4. 上传文档并开始提问

---

**文档版本：** 1.0
**最后更新：** 2026-03-24
**项目路径：** `C:\Users\xue\Desktop\opencode\rag-qa-system`

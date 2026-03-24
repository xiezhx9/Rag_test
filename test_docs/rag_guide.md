# RAG 技术详解

RAG (Retrieval-Augmented Generation) 是一种结合检索和生成的技术。

## 工作原理

1. **文档索引**：将文档分块并向量化存储
2. **查询检索**：根据问题检索相关文档块
3. **答案生成**：LLM 基于检索结果生成答案

## 核心组件

### 向量数据库
- Chroma：轻量级，适合小规模
- Milvus：高性能，适合大规模
- Pinecone：云端托管

### Embedding 模型
- BGE-M3：中文友好，混合检索
- OpenAI text-embedding-3：API 调用
- GTE：轻量级选择

## 最佳实践

1. 合理设置分块大小（通常 256-1024 tokens）
2. 使用重叠保持上下文连贯
3. 选择适合语言的 Embedding 模型
4. 调整 top_k 参数优化检索效果

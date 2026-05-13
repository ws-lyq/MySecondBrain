# LangChain 学习总结

## 核心概念
LangChain 是一个用于构建 LLM 应用的框架，核心抽象包括：

### 1. Models（模型）
- **LLM**：纯文本生成模型（如 DeepSeek、GPT-3.5）
- **Chat Models**：对话模型，支持多轮消息
- **Embeddings**：文本向量化模型

### 2. Prompts（提示词）
- **PromptTemplate**：提示词模板，支持变量插值
- **ChatPromptTemplate**：对话类提示词模板

### 3. Chains（链）
将多个组件串联成流水线。例如 RetrievalQA Chain：
```
用户输入 → 向量检索 → prompt 组装 → LLM 调用 → 输出
```

### 4. Document Loaders（文档加载器）
- `TextLoader`：加载纯文本文件
- `DirectoryLoader`：批量加载目录下所有文件
- `PyPDFLoader`：加载 PDF 文件
- `UnstructuredMarkdownLoader`：加载 Markdown 文件

### 5. Text Splitters（文本切分器）
- `RecursiveCharacterTextSplitter`：递归式按分隔符切分
- `CharacterTextSplitter`：按固定字符数切分
- `MarkdownHeaderTextSplitter`：按 Markdown 标题结构切分

### 6. Vector Stores（向量存储）
- Chroma（本地，开源）
- FAISS（本地，高性能）
- Pinecone（云端，托管）

### 7. Retrievers（检索器）
- `vectorstore.as_retriever()`：最基础的向量检索
- `MultiQueryRetriever`：从多个角度生成查询
- `ContextualCompressionRetriever`：压缩检索结果

## 常用的 Chain Type
- **stuff**：将所有文档一次性塞入 prompt（简单但受限于上下文窗口）
- **map_reduce**：先对每个文档独立处理，再汇总结果
- **refine**：逐文档迭代优化回答
- **map_rerank**：对每个文档打分，取最高分结果

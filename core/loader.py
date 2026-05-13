import os
from typing import List
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
import config
from .embeddings import get_embeddings


def _get_glob_patterns():
    patterns = ["**/*.md", "**/*.txt"]
    try:
        import fitz
        patterns.append("**/*.pdf")
    except ImportError:
        pass
    try:
        import docx
        patterns.append("**/*.docx")
    except ImportError:
        pass
    return patterns


def build_knowledge_base():
    """加载 knowledge_base 目录下所有文档 → 切分 → 向量化 → 存入 ChromaDB"""
    print("📂 正在扫描知识库文件夹...")

    loader = DirectoryLoader(
        config.DATA_DIR,
        glob=_get_glob_patterns(),
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'},
        show_progress=True,
        recursive=True,
        use_multithreading=True
    )
    docs = loader.load()
    print(f"📄 成功加载 {len(docs)} 个文档")

    if not docs:
        print("⚠️ 知识库为空，请先在 knowledge_base 中添加笔记")
        return None

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
    )
    splits = text_splitter.split_documents(docs)

    print("🚀 正在向量化并入库...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=get_embeddings(),
        persist_directory=config.DB_DIR
    )
    print("✅ 知识库构建完成！")
    return vectorstore


def load_single_document(file_path: str) -> List[Document]:
    """加载单个文件（支持 .md / .txt / .pdf / .docx）"""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyMuPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    return loader.load()


def add_document_to_knowledge_base(file_path: str) -> bool:
    """将单个文件向量化后追加到现有知识库"""
    docs = load_single_document(file_path)
    if not docs:
        return False

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
    )
    splits = text_splitter.split_documents(docs)

    vectorstore = Chroma(
        persist_directory=config.DB_DIR,
        embedding_function=get_embeddings()
    )
    vectorstore.add_documents(splits)
    return True


def get_indexed_files() -> List[str]:
    """返回知识库目录下的源文件列表（按文件路径扫描，不依赖向量库）"""
    if not os.path.exists(config.DATA_DIR):
        return []

    extensions = (".md", ".txt", ".pdf", ".docx")
    files = []
    for root, _, filenames in os.walk(config.DATA_DIR):
        for f in filenames:
            if f.lower().endswith(extensions):
                files.append(os.path.join(root, f))
    return sorted(files)

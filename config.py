import os
from pathlib import Path
from dotenv import load_dotenv

# 项目根目录（config.py 所在目录）
PROJECT_ROOT = Path(__file__).parent.resolve()

load_dotenv(PROJECT_ROOT / "key.env")

# Paths（基于项目根目录）
DATA_DIR = os.getenv("DATA_DIR", str(PROJECT_ROOT / "knowledge_base"))
DB_DIR = os.getenv("DB_DIR", str(PROJECT_ROOT / "vector_db"))

# LLM
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Embedding
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")

# Retrieval
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "3"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

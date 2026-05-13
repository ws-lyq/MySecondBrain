import os
os.environ.setdefault('HF_ENDPOINT', 'https://hf-mirror.com')
os.environ.setdefault('TRANSFORMERS_OFFLINE', '1')
os.environ.setdefault('HF_HUB_OFFLINE', '1')

from langchain_huggingface import HuggingFaceEmbeddings
import config


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={'device': config.EMBEDDING_DEVICE},
        encode_kwargs={'normalize_embeddings': True}
    )

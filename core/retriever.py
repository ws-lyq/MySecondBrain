import os
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
import config
from .llm import get_llm
from .embeddings import get_embeddings
from .loader import build_knowledge_base


def create_qa_chain(vectorstore, streaming: bool = False):
    llm = get_llm(streaming=streaming)
    retriever = vectorstore.as_retriever(search_kwargs={"k": config.RETRIEVAL_TOP_K})
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff"
    )


def get_qa_chain(streaming: bool = False):
    if not os.path.exists(config.DB_DIR):
        vectorstore = build_knowledge_base()
    else:
        vectorstore = Chroma(
            persist_directory=config.DB_DIR,
            embedding_function=get_embeddings()
        )
    return create_qa_chain(vectorstore, streaming=streaming), vectorstore

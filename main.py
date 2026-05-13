import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from langchain_chroma import Chroma
import config
from core import build_knowledge_base, get_embeddings
from core.retriever import create_qa_chain


def run_chat(vectorstore):
    llm_kwargs = {"k": config.RETRIEVAL_TOP_K}
    retriever = vectorstore.as_retriever(search_kwargs=llm_kwargs)
    qa_chain = create_qa_chain(vectorstore)

    print("\n" + "=" * 30)
    print("🤖 你的个人知识库已就绪！")
    print("输入 'exit' 退出，输入 'refresh' 重新加载知识库")
    print("=" * 30)

    while True:
        query = input("\n👤 我: ").strip()
        if query.lower() == "exit":
            break
        if query.lower() == "refresh":
            print("🔄 重新构建知识库...")
            vectorstore = build_knowledge_base()
            if vectorstore is None:
                continue
            retriever = vectorstore.as_retriever(search_kwargs=llm_kwargs)
            qa_chain = create_qa_chain(vectorstore)
            continue

        if not query:
            continue

        result = qa_chain.invoke({"query": query})
        print(f"🤖 AI: {result['result']}")

        if result.get('source_documents'):
            print("📚 参考资料:")
            for i, doc in enumerate(result['source_documents']):
                source = doc.metadata.get('source', '未知文件')
                filename = source.replace('\\', '/').split('/')[-1]
                print(f"  [{i + 1}] {filename}")


if __name__ == "__main__":
    if not os.path.exists(config.DB_DIR):
        vectorstore = build_knowledge_base()
    else:
        print("⚡ 检测到已有知识库，直接加载...")
        vectorstore = Chroma(
            persist_directory=config.DB_DIR,
            embedding_function=get_embeddings()
        )

    if vectorstore is None:
        print("❌ 知识库为空，程序退出")
    else:
        run_chat(vectorstore)

import os
import sys

# 必须放在所有导入之前：强制 HuggingFace 离线模式（模型已本地缓存）
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

import tempfile
import streamlit as st
from langchain_core.callbacks import BaseCallbackHandler
from core import get_qa_chain, create_qa_chain, build_knowledge_base
from core import add_document_to_knowledge_base, get_indexed_files
import config

st.set_page_config(page_title="个人知识库问答", page_icon="🧠", layout="wide")
st.title("🧠 My Second Brain - 个人知识库问答")


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "qa_chain" not in st.session_state:
        with st.spinner("正在加载知识库..."):
            qa_chain, vectorstore = get_qa_chain(streaming=True)
            st.session_state.qa_chain = qa_chain
            st.session_state.vectorstore = vectorstore
            st.session_state.kb_ready = True
    if "kb_ready" not in st.session_state:
        st.session_state.kb_ready = False


# ==================== 侧边栏 ====================
with st.sidebar:
    st.subheader("📚 知识库管理")

    if st.button("🔄 重建知识库", use_container_width=True):
        with st.spinner("正在重新构建..."):
            new_vs = build_knowledge_base()
            if new_vs:
                new_qc = create_qa_chain(new_vs, streaming=True)
                st.session_state.vectorstore = new_vs
                st.session_state.qa_chain = new_qc
                st.session_state.messages = []
                st.success("知识库已更新！")
                st.rerun()

    st.divider()
    st.subheader("📎 上传文档")
    uploaded_file = st.file_uploader(
        "支持 PDF / Word / Markdown / 文本",
        type=["pdf", "docx", "md", "txt"],
        label_visibility="collapsed",
        key="file_uploader",
    )

    if uploaded_file:
        suffix = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        dest_dir = os.path.join(config.DATA_DIR, "3-Resources", "上传文件")
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, uploaded_file.name)
        with open(dest_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        success = add_document_to_knowledge_base(tmp_path)
        os.unlink(tmp_path)

        if success:
            new_vs = st.session_state.vectorstore
            new_qc = create_qa_chain(new_vs, streaming=True)
            st.session_state.qa_chain = new_qc
            st.success(f"✅ 已添加「{uploaded_file.name}」")
            st.rerun()
        else:
            st.error("文件处理失败")

    st.divider()
    st.subheader("📋 已索引文件")

    if st.session_state.get("kb_ready", False):
        try:
            indexed = get_indexed_files()
            if indexed:
                for f in indexed:
                    short = f.replace("\\", "/").split("/")[-1]
                    st.caption(f"📄 {short}")
            else:
                st.caption("暂无索引文件")
        except Exception as e:
            st.caption(f"加载索引列表失败: {e}")
    else:
        st.caption("等待知识库加载...")


# ==================== 主界面 ====================
init_session()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "source_documents" in msg:
            with st.expander("📚 参考资料"):
                for i, doc in enumerate(msg["source_documents"]):
                    source = doc.metadata.get("source", "未知文件")
                    filename = source.replace("\\", "/").split("/")[-1]
                    st.write(f"{i+1}. {filename}")

if prompt := st.chat_input("请输入你的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()
        stream_handler = StreamHandler(response_container)

        try:
            result = st.session_state.qa_chain.invoke(
                {"query": prompt},
                config={"callbacks": [stream_handler]},
            )
            answer = result["result"]
            source_docs = result.get("source_documents", [])

            if source_docs:
                with st.expander("📚 参考资料"):
                    for i, doc in enumerate(source_docs):
                        source = doc.metadata.get("source", "未知文件")
                        filename = source.replace("\\", "/").split("/")[-1]
                        st.write(f"{i+1}. {filename}")

        except Exception as e:
            answer = f"❌ 发生错误：{str(e)}"
            st.error(answer)
            source_docs = []

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "source_documents": source_docs,
            }
        )

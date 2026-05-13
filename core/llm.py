from langchain_deepseek import ChatDeepSeek
import config


def get_llm(streaming: bool = False):
    return ChatDeepSeek(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        api_key=config.DEEPSEEK_API_KEY,
        streaming=streaming
    )

from functools import lru_cache

from langchain_deepseek import ChatDeepSeek

from app.core.config import settings


@lru_cache
def get_llm() -> ChatDeepSeek:
    return ChatDeepSeek(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
        api_key=settings.llm_api_key,
        extra_body={"thinking": {"type": "disabled"}},
    )

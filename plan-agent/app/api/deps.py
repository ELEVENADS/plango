from functools import lru_cache

from elasticsearch import Elasticsearch
from langchain_deepseek import ChatDeepSeek

from app.core.config import settings
from app.rag.config import get_embedding_model
from app.rag.pipeline import RAGPipeline
from app.tools.search import init_rag_tool


@lru_cache
def get_llm() -> ChatDeepSeek:
    return ChatDeepSeek(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
        api_key=settings.llm_api_key,
        extra_body={"thinking": {"type": "disabled"}},
    )


@lru_cache
def get_es_client() -> Elasticsearch:
    return Elasticsearch(settings.elasticsearch_url)


@lru_cache
def get_rag_pipeline() -> RAGPipeline:
    es = get_es_client()
    embedding = get_embedding_model()
    llm = get_llm()
    pipeline = RAGPipeline(es, embedding, llm)
    init_rag_tool(pipeline)
    return pipeline

from functools import lru_cache

from langchain_openai import OpenAIEmbeddings
from pydantic import Field
from pydantic_settings import BaseSettings

from app.core.config import settings


class RAGSettings(BaseSettings):
    """RAG-specific configuration, loaded from env / .env."""

    # Embedding model (OpenAI-compatible API)
    embedding_api_key: str = ""
    embedding_api_base: str = "https://api.openai.com/v1"
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536

    # Elasticsearch index
    index_name: str = "plango_plans"

    # Retrieval
    retrieval_top_k: int = 5
    bm25_weight: float = 0.3
    vector_weight: float = 0.7

    # Query expansion
    query_expansion_enabled: bool = True
    query_expansion_variants: int = 3

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


rag_settings = RAGSettings()


@lru_cache
def get_embedding_model() -> OpenAIEmbeddings:
    api_key = rag_settings.embedding_api_key or settings.llm_api_key
    return OpenAIEmbeddings(
        model=rag_settings.embedding_model,
        api_key=api_key,
        base_url=rag_settings.embedding_api_base,
        dimensions=rag_settings.embedding_dim,
    )

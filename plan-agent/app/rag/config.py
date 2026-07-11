from functools import lru_cache

from langchain_openai import OpenAIEmbeddings
from pydantic import Field
from pydantic_settings import BaseSettings

from app.core.config import settings


class RAGSettings(BaseSettings):
    """RAG-specific configuration, loaded from env / .env."""

    # Embedding provider: ollama (local, default) or openai (online)
    embedding_provider: str = "ollama"

    # Ollama embedding (local)
    ollama_embedding_base_url: str = "http://localhost:11434/v1"
    ollama_embedding_model: str = "qwen3-embedding:4b"
    ollama_embedding_dim: int = 2048

    # OpenAI embedding (online, used when embedding_provider=openai)
    embedding_api_key: str = ""
    embedding_api_base: str = "https://api.openai.com/v1"
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536

    # Elasticsearch indices
    index_name: str = "plango_plans"
    knowledge_index_name: str = "plango_knowledge"

    # Chunking
    chunk_size: int = 500
    chunk_overlap: int = 50

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
    if rag_settings.embedding_provider == "ollama":
        return OpenAIEmbeddings(
            model=rag_settings.ollama_embedding_model,
            base_url=rag_settings.ollama_embedding_base_url,
            api_key="ollama",
        )
    else:
        api_key = rag_settings.embedding_api_key or settings.llm_api_key
        return OpenAIEmbeddings(
            model=rag_settings.embedding_model,
            api_key=api_key,
            base_url=rag_settings.embedding_api_base,
            dimensions=rag_settings.embedding_dim,
        )


def get_embedding_dim() -> int:
    """Return the current provider's embedding dimension for ES index mapping."""
    if rag_settings.embedding_provider == "ollama":
        return rag_settings.ollama_embedding_dim
    return rag_settings.embedding_dim

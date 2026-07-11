from elasticsearch import Elasticsearch

from app.rag.config import get_embedding_dim, rag_settings


def build_mapping(dims: int | None = None) -> dict:
    """Build the ES index mapping for plan documents.

    The mapping supports both BM25 (text) and dense vector (kNN) retrieval.
    IK analyzer is used for Chinese text fields; falls back to standard if
    the IK plugin is not installed on the ES node.
    """
    dims = dims or get_embedding_dim()
    return {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "refresh_interval": "5s",
        },
        "mappings": {
            "properties": {
                "plan_id": {"type": "long"},
                "user_id": {"type": "long"},
                "title": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_smart",
                    "fields": {
                        "keyword": {"type": "keyword"},
                    },
                },
                "description": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_smart",
                },
                "plan_date": {"type": "date", "format": "yyyy-MM-dd"},
                "start_time": {"type": "keyword"},
                "end_time": {"type": "keyword"},
                "priority": {"type": "integer"},
                "status": {"type": "keyword"},
                "tags": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_smart",
                },
                "ai_feedback": {"type": "text"},
                "ai_generated": {"type": "boolean"},
                "deleted": {"type": "boolean"},
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": dims,
                    "index": True,
                    "similarity": "cosine",
                },
                "embedding_text": {"type": "text"},
            }
        },
    }


def build_knowledge_mapping(dims: int | None = None) -> dict:
    """Build the ES index mapping for generic knowledge documents.

    Supports multiple doc types (preference, rule, resource) plus
    chunk-level tracking for long text splitting.
    """
    dims = dims or get_embedding_dim()
    return {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "refresh_interval": "5s",
        },
        "mappings": {
            "properties": {
                "doc_id": {"type": "keyword"},
                "user_id": {"type": "long"},
                "doc_type": {"type": "keyword"},
                "title": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_smart",
                    "fields": {"keyword": {"type": "keyword"}},
                },
                "content": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_smart",
                },
                "tags": {
                    "type": "text",
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_smart",
                },
                "source": {"type": "keyword"},
                "chunk_index": {"type": "integer"},
                "parent_id": {"type": "keyword"},
                "metadata": {"type": "object", "enabled": False},
                "embedding": {
                    "type": "dense_vector",
                    "dims": dims,
                    "index": True,
                    "similarity": "cosine",
                },
                "embedding_text": {"type": "text"},
                "deleted": {"type": "boolean"},
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"},
            }
        },
    }


def create_index(es: Elasticsearch, index_name: str | None = None, dims: int | None = None) -> str:
    """Create the ES plan index if it does not already exist. Returns the index name."""
    index_name = index_name or rag_settings.index_name
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=build_mapping(dims))
    return index_name


def create_knowledge_index(es: Elasticsearch, dims: int | None = None) -> str:
    """Create the ES knowledge index if it does not already exist. Returns the index name."""
    index_name = rag_settings.knowledge_index_name
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=build_knowledge_mapping(dims))
    return index_name


def delete_index(es: Elasticsearch, index_name: str | None = None) -> None:
    """Delete the ES index. Use with caution."""
    index_name = index_name or rag_settings.index_name
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)


def refresh_index(es: Elasticsearch, index_name: str | None = None) -> None:
    """Force-refresh the index so newly indexed documents become visible."""
    index_name = index_name or rag_settings.index_name
    es.indices.refresh(index=index_name)

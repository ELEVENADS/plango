from elasticsearch import Elasticsearch

from app.rag.config import rag_settings


def build_mapping(dims: int | None = None) -> dict:
    """Build the ES index mapping for plan documents.

    The mapping supports both BM25 (text) and dense vector (kNN) retrieval.
    IK analyzer is used for Chinese text fields; falls back to standard if
    the IK plugin is not installed on the ES node.
    """
    dims = dims or rag_settings.embedding_dim
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


def create_index(es: Elasticsearch, index_name: str | None = None, dims: int | None = None) -> str:
    """Create the ES index if it does not already exist. Returns the index name."""
    index_name = index_name or rag_settings.index_name
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=build_mapping(dims))
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

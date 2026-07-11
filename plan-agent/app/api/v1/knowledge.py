from fastapi import APIRouter, HTTPException

from app.api.deps import get_es_client
from app.models.knowledge_request import KnowledgeSyncRequest
from app.rag.config import get_embedding_model
from app.rag.ingestion import DocumentIngester

router = APIRouter(prefix="/rag/knowledge", tags=["rag-knowledge"])

_ingester: DocumentIngester | None = None


def _get_ingester() -> DocumentIngester:
    global _ingester
    if _ingester is None:
        _ingester = DocumentIngester(get_es_client(), get_embedding_model())
    return _ingester


@router.post("", status_code=204)
async def sync_knowledge(request: KnowledgeSyncRequest) -> None:
    ingester = _get_ingester()
    try:
        await ingester.ingest_knowledge(request.to_doc_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index knowledge: {e}")


@router.delete("/{doc_id}", status_code=204)
async def delete_knowledge(doc_id: str) -> None:
    ingester = _get_ingester()
    try:
        await ingester.delete_knowledge(doc_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete knowledge: {e}")

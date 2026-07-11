from fastapi import APIRouter, HTTPException

from app.api.deps import get_es_client
from app.models.rag_request import PlanSyncRequest
from app.rag.config import get_embedding_model
from app.rag.ingestion import DocumentIngester

router = APIRouter(prefix="/rag", tags=["rag"])

_ingester: DocumentIngester | None = None


def _get_ingester() -> DocumentIngester:
    global _ingester
    if _ingester is None:
        _ingester = DocumentIngester(get_es_client(), get_embedding_model())
    return _ingester


@router.post("/plans", status_code=204)
async def sync_plan(request: PlanSyncRequest) -> None:
    ingester = _get_ingester()
    try:
        await ingester.ingest_plan(request.to_plan_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index plan: {e}")


@router.delete("/plans/{plan_id}", status_code=204)
async def delete_plan(plan_id: int) -> None:
    ingester = _get_ingester()
    try:
        await ingester.delete_plan(plan_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete plan: {e}")

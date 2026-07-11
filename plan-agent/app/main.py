from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.v1.generate import router as generate_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.rag import router as rag_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.rag.indexing import create_index, create_knowledge_index
from app.registry import register_service, deregister_service

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from elasticsearch import Elasticsearch

    register_service()
    es = Elasticsearch(settings.elasticsearch_url)
    create_index(es)
    create_knowledge_index(es)
    es.close()
    yield
    deregister_service()


app = FastAPI(title="PlanGoDaily Agent", version="1.0.0", lifespan=lifespan)

app.include_router(generate_router, prefix="/api/v1")
app.include_router(rag_router, prefix="/api/v1")
app.include_router(knowledge_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"service": "PlanGoDaily Agent", "status": "running"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=18000,
        reload=True,
    )

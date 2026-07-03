from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings

from app.rag.config import rag_settings


class DocumentIngester:
    """Handles ingestion of plan documents into Elasticsearch with embeddings.

    Supports single and batch indexing, updates, and deletes.
    Embedding text is built from the plan's title, description, and tags.
    """

    def __init__(
        self,
        es: Elasticsearch,
        embedding_model: OpenAIEmbeddings,
        index_name: str | None = None,
    ) -> None:
        self.es = es
        self.embedding_model = embedding_model
        self.index_name = index_name or rag_settings.index_name

    @staticmethod
    def build_embedding_text(plan: dict) -> str:
        """Build the text that will be embedded for dense retrieval."""
        parts = [plan.get("title", "")]
        desc = plan.get("description")
        if desc:
            parts.append(desc)
        tags = plan.get("tags")
        if tags:
            parts.append(tags)
        return " ".join(parts)

    async def ingest_plan(self, plan: dict) -> None:
        """Index a single plan document with its embedding vector."""
        text = self.build_embedding_text(plan)
        embedding = await self.embedding_model.aembed_query(text)
        doc = {**plan, "embedding": embedding, "embedding_text": text}
        self.es.index(
            index=self.index_name,
            id=str(plan["plan_id"]),
            body=doc,
            refresh=False,
        )

    async def ingest_batch(self, plans: list[dict]) -> int:
        """Batch-index multiple plans. Returns the count of indexed documents."""
        if not plans:
            return 0

        texts = [self.build_embedding_text(p) for p in plans]
        embeddings = await self.embedding_model.aembed_documents(texts)

        from elasticsearch.helpers import bulk

        actions = []
        for i, (plan, embedding) in enumerate(zip(plans, embeddings)):
            doc = {**plan, "embedding": embedding, "embedding_text": texts[i]}
            actions.append({
                "_index": self.index_name,
                "_id": str(plan["plan_id"]),
                "_source": doc,
            })

        success, _ = bulk(self.es, actions, refresh=False)
        return success

    async def update_plan(self, plan: dict) -> None:
        """Upsert a plan document (re-index with updated embedding)."""
        await self.ingest_plan(plan)

    async def delete_plan(self, plan_id: int) -> None:
        """Remove a plan document from the index."""
        self.es.delete(index=self.index_name, id=str(plan_id))

    async def delete_batch(self, plan_ids: list[int]) -> int:
        """Remove multiple plan documents. Returns count of deleted docs."""
        if not plan_ids:
            return 0

        from elasticsearch.helpers import bulk

        actions = [
            {"_op_type": "delete", "_index": self.index_name, "_id": str(pid)}
            for pid in plan_ids
        ]
        success, _ = bulk(self.es, actions, refresh=False)
        return success

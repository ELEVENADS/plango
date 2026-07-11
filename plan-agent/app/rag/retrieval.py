from elasticsearch import Elasticsearch
from langchain_openai import OpenAIEmbeddings

from app.rag.config import rag_settings


class HybridRetriever:
    """Hybrid retrieval combining BM25 (sparse) and kNN (dense vector) search.

    Runs both searches in parallel across plan and knowledge indices,
    normalizes scores per-result-set, and fuses them with configurable weights.
    """

    def __init__(
        self,
        es: Elasticsearch,
        embedding_model: OpenAIEmbeddings,
        index_name: str | None = None,
        top_k: int | None = None,
        bm25_weight: float | None = None,
        vector_weight: float | None = None,
    ) -> None:
        self.es = es
        self.embedding_model = embedding_model
        self.index_name = index_name or rag_settings.index_name
        self.knowledge_index = rag_settings.knowledge_index_name
        self.top_k = top_k or rag_settings.retrieval_top_k
        self.bm25_weight = bm25_weight or rag_settings.bm25_weight
        self.vector_weight = vector_weight or rag_settings.vector_weight

    @property
    def _search_indices(self) -> str:
        """Comma-separated list of indices to search across."""
        return f"{self.index_name},{self.knowledge_index}"

    async def retrieve(self, query: str, user_id: int) -> list[dict]:
        """Run hybrid search and return ranked plan documents."""
        import asyncio

        bm25_task = asyncio.create_task(
            asyncio.to_thread(self._bm25_search, query, user_id)
        )
        vector_task = asyncio.create_task(self._vector_search(query, user_id))

        bm25_results, vector_results = await bm25_task, await vector_task

        combined = self._fuse_scores(bm25_results, vector_results)
        return combined[: self.top_k]

    async def bm25_only(self, query: str, user_id: int) -> list[dict]:
        """Run BM25-only search (sparse retrieval)."""
        import asyncio
        return await asyncio.to_thread(self._bm25_search, query, user_id)

    async def vector_only(self, query: str, user_id: int) -> list[dict]:
        """Run kNN-only search (dense retrieval)."""
        return await self._vector_search(query, user_id)

    # ── internals ─────────────────────────────────────────────────

    def _bm25_search(self, query: str, user_id: int) -> list[dict]:
        body = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"user_id": user_id}},
                        {"term": {"deleted": False}},
                    ],
                    "should": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": [
                                    "title^3",
                                    "description^2",
                                    "content^2",
                                    "tags",
                                ],
                                "type": "best_fields",
                            }
                        }
                    ],
                }
            },
            "size": self.top_k,
            "_source": {"excludes": ["embedding"]},
        }
        resp = self.es.search(index=self._search_indices, body=body)
        return [
            {"id": h["_id"], "score": h["_score"] or 0.0, **h["_source"]}
            for h in resp["hits"]["hits"]
        ]

    async def _vector_search(self, query: str, user_id: int) -> list[dict]:
        import asyncio

        query_embedding = await self.embedding_model.aembed_query(query)

        body = {
            "knn": {
                "field": "embedding",
                "query_vector": query_embedding,
                "k": self.top_k,
                "num_candidates": self.top_k * 5,
                "filter": [
                    {"term": {"user_id": user_id}},
                    {"term": {"deleted": False}},
                ],
            },
            "size": self.top_k,
            "_source": {"excludes": ["embedding"]},
        }
        resp = await asyncio.to_thread(self.es.search, index=self._search_indices, body=body)
        return [
            {"id": h["_id"], "score": h["_score"] or 0.0, **h["_source"]}
            for h in resp["hits"]["hits"]
        ]

    def _fuse_scores(
        self, bm25_results: list[dict], vector_results: list[dict]
    ) -> list[dict]:
        """Weighted score fusion with min-max normalization per result set."""
        merged: dict[str, dict] = {}
        for r in bm25_results:
            merged[r["id"]] = {**r, "_bm25_score": r["score"], "_vector_score": 0.0}
        for r in vector_results:
            if r["id"] in merged:
                merged[r["id"]]["_vector_score"] = r["score"]
            else:
                merged[r["id"]] = {**r, "_bm25_score": 0.0, "_vector_score": r["score"]}

        # Normalize each score set
        bm25_scores = [v["_bm25_score"] for v in merged.values()]
        vector_scores = [v["_vector_score"] for v in merged.values()]

        bm25_min, bm25_max = (min(bm25_scores), max(bm25_scores)) if bm25_scores else (0, 1)
        vec_min, vec_max = (min(vector_scores), max(vector_scores)) if vector_scores else (0, 1)

        for doc in merged.values():
            n_bm25 = _normalize(doc["_bm25_score"], bm25_min, bm25_max)
            n_vec = _normalize(doc["_vector_score"], vec_min, vec_max)
            doc["_combined_score"] = self.bm25_weight * n_bm25 + self.vector_weight * n_vec

        ranked = sorted(merged.values(), key=lambda d: d["_combined_score"], reverse=True)
        return ranked


def _normalize(value: float, vmin: float, vmax: float) -> float:
    if vmax == vmin:
        return 1.0 if value > 0 else 0.0
    return (value - vmin) / (vmax - vmin)

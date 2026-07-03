from unittest.mock import AsyncMock, MagicMock

import pytest

from app.rag.retrieval import HybridRetriever, _normalize


class TestNormalize:
    def test_mid_range(self) -> None:
        assert _normalize(5.0, 0.0, 10.0) == 0.5

    def test_min_value(self) -> None:
        assert _normalize(0.0, 0.0, 10.0) == 0.0

    def test_max_value(self) -> None:
        assert _normalize(10.0, 0.0, 10.0) == 1.0

    def test_single_value(self) -> None:
        assert _normalize(5.0, 5.0, 5.0) == 1.0

    def test_zero_value_when_all_zero(self) -> None:
        assert _normalize(0.0, 0.0, 0.0) == 0.0


class TestFuseScores:
    def test_bm25_only(self) -> None:
        bm25 = [
            {"id": "1", "score": 10.0, "title": "A", "_bm25_score": 0.0, "_vector_score": 0.0},
            {"id": "2", "score": 5.0, "title": "B", "_bm25_score": 0.0, "_vector_score": 0.0},
        ]
        vector: list[dict] = []
        retriever = HybridRetriever(None, None)
        fused = retriever._fuse_scores(bm25, vector)
        assert len(fused) == 2
        assert fused[0]["id"] == "1"

    def test_vector_only(self) -> None:
        bm25: list[dict] = []
        vector = [
            {"id": "1", "score": 0.9, "title": "A", "_bm25_score": 0.0, "_vector_score": 0.0},
            {"id": "2", "score": 0.7, "title": "B", "_bm25_score": 0.0, "_vector_score": 0.0},
        ]
        retriever = HybridRetriever(None, None)
        fused = retriever._fuse_scores(bm25, vector)
        assert len(fused) == 2
        assert fused[0]["id"] == "1"

    def test_hybrid_deduplicates(self) -> None:
        bm25 = [
            {"id": "1", "score": 10.0, "title": "A", "_bm25_score": 0.0, "_vector_score": 0.0},
            {"id": "2", "score": 3.0, "title": "B", "_bm25_score": 0.0, "_vector_score": 0.0},
        ]
        vector = [
            {"id": "1", "score": 0.8, "title": "A", "_bm25_score": 0.0, "_vector_score": 0.0},
            {"id": "3", "score": 0.5, "title": "C", "_bm25_score": 0.0, "_vector_score": 0.0},
        ]
        retriever = HybridRetriever(None, None)
        fused = retriever._fuse_scores(bm25, vector)
        assert len(fused) == 3

    def test_weight_configuration(self) -> None:
        retriever = HybridRetriever(None, None, bm25_weight=0.8, vector_weight=0.2)
        assert retriever.bm25_weight == 0.8
        assert retriever.vector_weight == 0.2


class TestRetrieve:
    @pytest.mark.asyncio
    async def test_bm25_only(self, mock_embedding_model) -> None:
        es = MagicMock()
        es.search.return_value = {
            "hits": {
                "hits": [
                    {"_id": "1", "_score": 5.0, "_source": {"title": "Java学习", "user_id": 100, "deleted": False}},
                ]
            }
        }

        retriever = HybridRetriever(es, mock_embedding_model, "test_index")
        results = await retriever.bm25_only("Java", 100)

        assert len(results) == 1
        assert results[0]["title"] == "Java学习"

    @pytest.mark.asyncio
    async def test_vector_only(self, mock_embedding_model) -> None:
        es = MagicMock()
        es.search.return_value = {
            "hits": {
                "hits": [
                    {"_id": "1", "_score": 0.92, "_source": {"title": "健身", "user_id": 100, "deleted": False}},
                ]
            }
        }

        retriever = HybridRetriever(es, mock_embedding_model, "test_index")
        results = await retriever.vector_only("运动", 100)

        assert len(results) == 1
        assert results[0]["title"] == "健身"
        mock_embedding_model.aembed_query.assert_called_once_with("运动")

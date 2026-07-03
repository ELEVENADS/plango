from unittest.mock import AsyncMock, MagicMock

import pytest

from app.rag.pipeline import RAGPipeline


class TestFormatContext:
    def test_empty_docs(self) -> None:
        result = RAGPipeline._format_context([])
        assert result == ""

    def test_single_doc_full(self) -> None:
        doc = {
            "title": "Java学习",
            "description": "学习Spring Boot",
            "plan_date": "2026-07-03",
            "start_time": "09:00",
            "end_time": "11:00",
            "tags": "学习,Java",
        }
        result = RAGPipeline._format_context([doc])
        assert "标题：Java学习" in result
        assert "描述：学习Spring Boot" in result
        assert "2026-07-03" in result
        assert "09:00" in result
        assert "11:00" in result
        assert "标签：学习,Java" in result

    def test_single_doc_minimal(self) -> None:
        doc = {"title": "跑步", "plan_date": "2026-07-03", "start_time": "", "end_time": ""}
        result = RAGPipeline._format_context([doc])
        assert "标题：跑步" in result
        assert "描述：" not in result
        assert "标签：" not in result


class TestRun:
    @pytest.mark.asyncio
    async def test_run_expanded(self, mock_embedding_model, mock_llm) -> None:
        es = MagicMock()
        es.search.return_value = {
            "hits": {
                "hits": [
                    {
                        "_id": "1",
                        "_score": 5.0,
                        "_source": {"title": "Java学习", "plan_date": "2026-07-03", "start_time": "09:00", "end_time": "11:00", "user_id": 100, "deleted": False},
                    }
                ]
            }
        }

        pipeline = RAGPipeline(es, mock_embedding_model, mock_llm, "test_index")
        context = await pipeline.run("给我安排今天的学习计划", user_id=100, expand=True)

        assert len(context) > 0
        assert "Java学习" in context

    @pytest.mark.asyncio
    async def test_run_no_expansion(self, mock_embedding_model, mock_llm) -> None:
        es = MagicMock()
        es.search.return_value = {
            "hits": {
                "hits": [
                    {
                        "_id": "1",
                        "_score": 5.0,
                        "_source": {"title": "健身", "plan_date": "2026-07-03", "start_time": "18:00", "end_time": "18:30", "user_id": 100, "deleted": False},
                    }
                ]
            }
        }

        pipeline = RAGPipeline(es, mock_embedding_model, mock_llm, "test_index")
        context = await pipeline.run("运动", user_id=100, expand=False)

        assert len(context) > 0
        assert "健身" in context

    @pytest.mark.asyncio
    async def test_run_empty_results(self, mock_embedding_model, mock_llm) -> None:
        es = MagicMock()
        es.search.return_value = {"hits": {"hits": []}}

        pipeline = RAGPipeline(es, mock_embedding_model, mock_llm, "test_index")
        context = await pipeline.run("nonexistent query", user_id=999, expand=False)

        assert context == ""

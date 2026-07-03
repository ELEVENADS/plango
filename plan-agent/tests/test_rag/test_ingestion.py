import pytest

from app.rag.ingestion import DocumentIngester


class TestBuildEmbeddingText:
    def test_full_plan(self) -> None:
        plan = {
            "title": "学习Java",
            "description": "学习Spring Boot基础",
            "tags": "学习,Java",
        }
        text = DocumentIngester.build_embedding_text(plan)
        assert "学习Java" in text
        assert "Spring Boot" in text
        assert "学习,Java" in text

    def test_no_description(self) -> None:
        plan = {"title": "跑步", "tags": "运动"}
        text = DocumentIngester.build_embedding_text(plan)
        assert text == "跑步 运动"

    def test_no_tags(self) -> None:
        plan = {"title": "跑步", "description": "晨跑5公里"}
        text = DocumentIngester.build_embedding_text(plan)
        assert text == "跑步 晨跑5公里"

    def test_title_only(self) -> None:
        plan = {"title": "跑步"}
        text = DocumentIngester.build_embedding_text(plan)
        assert text == "跑步"


class TestIngestPlan:
    @pytest.mark.asyncio
    async def test_ingest_single(self, mock_es, mock_embedding_model) -> None:
        ingester = DocumentIngester(mock_es, mock_embedding_model, "test_index")
        plan = {
            "plan_id": 1,
            "user_id": 100,
            "title": "测试计划",
            "description": "测试描述",
            "tags": "测试",
            "plan_date": "2026-07-03",
        }
        await ingester.ingest_plan(plan)
        mock_es.index.assert_called_once()
        call_args = mock_es.index.call_args
        assert call_args[1]["index"] == "test_index"
        assert call_args[1]["id"] == "1"
        assert "embedding" in call_args[1]["body"]
        assert "embedding_text" in call_args[1]["body"]

    @pytest.mark.asyncio
    async def test_update_plan_delegates_to_ingest(self, mock_es, mock_embedding_model) -> None:
        ingester = DocumentIngester(mock_es, mock_embedding_model, "test_index")
        plan = {"plan_id": 1, "title": "更新的计划"}
        await ingester.update_plan(plan)
        mock_es.index.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_plan(self, mock_es, mock_embedding_model) -> None:
        ingester = DocumentIngester(mock_es, mock_embedding_model, "test_index")
        await ingester.delete_plan(1)
        mock_es.delete.assert_called_once_with(index="test_index", id="1")

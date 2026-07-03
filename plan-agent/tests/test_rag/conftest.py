from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def mock_es() -> MagicMock:
    """Mock Elasticsearch client."""
    es = MagicMock()
    es.indices.exists.return_value = False
    es.indices.create.return_value = {"acknowledged": True}
    es.indices.refresh.return_value = None
    es.indices.delete.return_value = {"acknowledged": True}
    es.index.return_value = {"_id": "1", "result": "created"}
    es.delete.return_value = {"result": "deleted"}
    return es


@pytest.fixture
def mock_embedding_model() -> MagicMock:
    """Mock embedding model that returns fixed-dimension vectors."""
    model = MagicMock()
    model.aembed_query = AsyncMock(return_value=[0.1] * 1536)
    model.aembed_documents = AsyncMock(return_value=[[0.1] * 1536])
    return model


@pytest.fixture
def mock_llm() -> MagicMock:
    """Mock LLM for query expansion."""
    llm = MagicMock()
    response = MagicMock()
    response.content = "学习计划安排\nJava学习路线\n日程规划建议"
    llm.ainvoke = AsyncMock(return_value=response)
    return llm


@pytest.fixture
def sample_plan() -> dict:
    return {
        "plan_id": 1,
        "user_id": 100,
        "title": "Java学习计划",
        "description": "学习Spring Boot框架基础",
        "plan_date": "2026-07-03",
        "start_time": "09:00",
        "end_time": "11:00",
        "priority": 2,
        "status": "PENDING",
        "tags": "学习,Java,Spring",
        "ai_generated": True,
        "ai_feedback": "",
        "deleted": False,
    }


@pytest.fixture
def sample_plans() -> list[dict]:
    return [
        {
            "plan_id": 1,
            "user_id": 100,
            "title": "Java学习",
            "description": "学习Spring Boot",
            "plan_date": "2026-07-03",
            "start_time": "09:00",
            "end_time": "11:00",
            "priority": 2,
            "status": "PENDING",
            "tags": "学习,Java",
            "ai_generated": True,
            "deleted": False,
        },
        {
            "plan_id": 2,
            "user_id": 100,
            "title": "健身锻炼",
            "description": "跑步30分钟",
            "plan_date": "2026-07-03",
            "start_time": "18:00",
            "end_time": "18:30",
            "priority": 1,
            "status": "PENDING",
            "tags": "运动,健康",
            "ai_generated": True,
            "deleted": False,
        },
    ]

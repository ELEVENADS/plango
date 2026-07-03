import pytest


@pytest.fixture
def sample_request() -> dict:
    return {
        "plan_id": 1,
        "user_id": 100,
        "title": "完成项目报告",
        "description": "需要在周五前完成Q2项目总结报告，大约10页",
    }

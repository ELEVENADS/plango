import pytest
from langchain_core.messages import HumanMessage


@pytest.fixture
def sample_messages() -> list[HumanMessage]:
    return [HumanMessage(content="帮我安排今天的学习计划")]

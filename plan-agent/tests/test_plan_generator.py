from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from langchain_core.messages import HumanMessage

from app.agents.plan_generator.schemas import PlanGeneratorState, StructuredPlanOutput


class TestPlanGenerateAgentGraph:
    def test_graph_builds(self) -> None:
        with patch("app.agents.plan_generator.graph.get_llm"), \
             patch("app.agents.plan_generator.graph.get_rag_pipeline"):
            from app.agents.plan_generator.graph import PlanGenerateAgent
            agent = PlanGenerateAgent()
            assert agent.graph is not None

    def test_should_summarize_below_threshold(self) -> None:
        with patch("app.agents.plan_generator.graph.get_llm"), \
             patch("app.agents.plan_generator.graph.get_rag_pipeline"):
            from app.agents.plan_generator.graph import PlanGenerateAgent

            agent = PlanGenerateAgent()
            state: PlanGeneratorState = {
                "messages": [HumanMessage(content="hi")],
                "user_id": 1,
                "rag_context": "",
                "memory_summary": "",
                "structured_output": StructuredPlanOutput(),
                "natural_output": "",
            }
            assert agent._should_summarize(state) == "skip"

    def test_should_summarize_above_threshold(self) -> None:
        with patch("app.agents.plan_generator.graph.get_llm"), \
             patch("app.agents.plan_generator.graph.get_rag_pipeline"):
            from app.agents.plan_generator.graph import PlanGenerateAgent

            agent = PlanGenerateAgent()
            messages = [HumanMessage(content=f"msg {i}") for i in range(15)]
            state: PlanGeneratorState = {
                "messages": messages,
                "user_id": 1,
                "rag_context": "",
                "memory_summary": "",
                "structured_output": StructuredPlanOutput(),
                "natural_output": "",
            }
            assert agent._should_summarize(state) == "summarize"

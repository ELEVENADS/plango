import pytest


class TestPlanGenerateAgent:
    def test_graph_builds(self) -> None:
        from app.agents.plan_generator.graph import PlanGenerateAgent
        agent = PlanGenerateAgent()
        assert agent.graph is not None

    @pytest.mark.asyncio
    async def test_ainvoke_returns_feedback(self, sample_request: dict) -> None:
        from app.agents.plan_generator.graph import PlanGenerateAgent

        agent = PlanGenerateAgent()
        result = await agent.ainvoke({
            "plan_id": sample_request["plan_id"],
            "user_id": sample_request["user_id"],
            "title": sample_request["title"],
            "description": sample_request["description"],
            "ai_feedback": "",
        })
        assert "ai_feedback" in result
        assert len(result["ai_feedback"]) > 0

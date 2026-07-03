from langgraph.graph import StateGraph, END

from app.agents.base import BaseAgent
from app.agents.plan_review.schemas import PlanReviewState


class PlanReviewAgent(BaseAgent):
    """Reviews completed plans. Placeholder for future implementation."""

    def __init__(self) -> None:
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(PlanReviewState)
        builder.add_node("review", self._review)
        builder.set_entry_point("review")
        builder.add_edge("review", END)
        return builder.compile()

    async def _review(self, state: PlanReviewState) -> dict:
        return {"review_feedback": ""}

    async def ainvoke(self, state: PlanReviewState) -> dict:
        return await self.graph.ainvoke(state)

    async def astream(self, state: PlanReviewState):
        async for chunk in self.graph.astream(state):
            yield chunk

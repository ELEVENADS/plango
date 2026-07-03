from langgraph.graph import StateGraph, END

from app.agents.base import BaseAgent
from app.agents.plan_generator.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.agents.plan_generator.schemas import PlanGeneratorState
from app.api.deps import get_llm


class PlanGenerateAgent(BaseAgent):
    """Generates AI feedback for a user's plan."""

    def __init__(self) -> None:
        self.llm = get_llm()
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(PlanGeneratorState)
        builder.add_node("generate_feedback", self._generate_feedback)
        builder.set_entry_point("generate_feedback")
        builder.add_edge("generate_feedback", END)
        return builder.compile()

    async def _generate_feedback(self, state: PlanGeneratorState) -> dict:
        prompt = USER_PROMPT_TEMPLATE.format(
            title=state["title"], description=state["description"]
        )
        response = await self.llm.ainvoke([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ])
        return {"ai_feedback": response.content}

    async def ainvoke(self, state: PlanGeneratorState) -> dict:
        return await self.graph.ainvoke(state)

    async def astream(self, state: PlanGeneratorState):
        async for chunk in self.graph.astream(state):
            yield chunk

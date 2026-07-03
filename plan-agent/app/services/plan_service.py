from langchain_core.messages import AIMessage, HumanMessage

from app.agents.plan_generator.graph import PlanGenerateAgent
from app.agents.plan_generator.schemas import PlanGeneratorState, StructuredPlanOutput
from app.models.request import PlanGenerateRequest
from app.models.response import PlanGenerateResponse


class PlanService:

    def __init__(self) -> None:
        self._agent = PlanGenerateAgent()

    async def generate(self, request: PlanGenerateRequest) -> PlanGenerateResponse:
        lc_messages = []
        for m in request.messages:
            if m.role == "user":
                lc_messages.append(HumanMessage(content=m.content))
            elif m.role == "assistant":
                lc_messages.append(AIMessage(content=m.content))

        state: PlanGeneratorState = {
            "messages": lc_messages,
            "user_id": request.user_id,
            "rag_context": "",
            "memory_summary": "",
            "structured_output": StructuredPlanOutput(),
            "natural_output": "",
        }

        result = await self._agent.ainvoke(state)
        return PlanGenerateResponse(
            natural_output=result.get("natural_output", ""),
            structured_output=result.get("structured_output", StructuredPlanOutput()),
        )

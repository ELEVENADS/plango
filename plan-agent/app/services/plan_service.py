from app.agents.plan_generator.graph import PlanGenerateAgent
from app.agents.plan_generator.schemas import PlanGeneratorState
from app.models.request import PlanGenerateRequest
from app.models.response import PlanGenerateResponse


class PlanService:

    def __init__(self) -> None:
        self._agent = PlanGenerateAgent()

    async def generate(self, request: PlanGenerateRequest) -> PlanGenerateResponse:
        state: PlanGeneratorState = {
            "plan_id": request.plan_id,
            "user_id": request.user_id,
            "title": request.title,
            "description": request.description,
            "ai_feedback": "",
        }
        result = await self._agent.ainvoke(state)
        return PlanGenerateResponse(
            plan_id=request.plan_id,
            ai_feedback=result.get("ai_feedback", ""),
        )

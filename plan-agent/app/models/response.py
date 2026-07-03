from pydantic import BaseModel


class PlanGenerateResponse(BaseModel):
    plan_id: int
    ai_feedback: str

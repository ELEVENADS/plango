from pydantic import BaseModel


class PlanGenerateRequest(BaseModel):
    plan_id: int
    user_id: int
    title: str
    description: str = ""

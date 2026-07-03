from typing import TypedDict


class PlanGeneratorState(TypedDict):
    plan_id: int
    user_id: int
    title: str
    description: str
    ai_feedback: str

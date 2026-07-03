from typing import TypedDict


class PlanReviewState(TypedDict):
    plan_id: int
    user_id: int
    review_feedback: str

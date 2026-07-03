from pydantic import BaseModel

from app.agents.plan_generator.schemas import StructuredPlanOutput


class PlanGenerateResponse(BaseModel):
    """Response from plan generation, containing both natural and structured output."""
    natural_output: str = ""
    structured_output: StructuredPlanOutput = StructuredPlanOutput()

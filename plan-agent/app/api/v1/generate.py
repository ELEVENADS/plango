from fastapi import APIRouter

from app.models.request import PlanGenerateRequest
from app.models.response import PlanGenerateResponse
from app.services.plan_service import PlanService

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("", response_model=PlanGenerateResponse)
async def generate_plan(request: PlanGenerateRequest) -> PlanGenerateResponse:
    service = PlanService()
    return await service.generate(request)

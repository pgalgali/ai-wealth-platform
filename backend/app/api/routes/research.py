from fastapi import APIRouter, Depends

from app.domain.services import CopilotService
from app.infrastructure.mock_adapters import MockResearchAdapter
from app.schemas.market import CopilotRequest, CopilotResponse

router = APIRouter(prefix="/v1/copilot", tags=["research copilot"])
copilot_service = CopilotService(MockResearchAdapter())


def get_copilot_service() -> CopilotService:
    return copilot_service


@router.post("/ask", response_model=CopilotResponse)
async def ask(request: CopilotRequest, service: CopilotService = Depends(get_copilot_service)) -> CopilotResponse:
    return await service.answer(request.question)

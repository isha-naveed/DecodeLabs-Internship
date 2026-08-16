from fastapi import APIRouter, HTTPException

from app.models.schemas import GenerationRequest, GenerationResponse
from app.services.generation_service import GenerationService


router = APIRouter(prefix="/api", tags=["Generation"])

generation_service = GenerationService()


@router.post("/generate", response_model=GenerationResponse)
async def generate_copy(request: GenerationRequest) -> GenerationResponse:
    try:
        return await generation_service.generate(request)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

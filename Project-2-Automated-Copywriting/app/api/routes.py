from fastapi import APIRouter, HTTPException

from app.models.schemas import GenerationRequest, GenerationResponse
from app.services.generation_service import GenerationService
from app.services.batch_pipeline import generate_batch


router = APIRouter(prefix="/api", tags=["Generation"])

generation_service = GenerationService()


@router.post("/generate", response_model=GenerationResponse)
async def generate_copy(
    request: GenerationRequest,
) -> GenerationResponse:
    try:
        return await generation_service.generate(request)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@router.post(
    "/generate-batch",
    response_model=list[GenerationResponse],
)
async def generate_batch_copy(
    requests: list[GenerationRequest],
) -> list[GenerationResponse]:
    try:
        return await generate_batch(requests)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc
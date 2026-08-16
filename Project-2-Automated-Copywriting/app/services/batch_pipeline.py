import asyncio

from app.config import settings
from app.models.schemas import GenerationRequest, GenerationResponse
from app.services.generation_service import GenerationService


async def generate_batch(
    requests: list[GenerationRequest],
    max_concurrent: int | None = None,
) -> list[GenerationResponse]:
    service = GenerationService()

    limit = max_concurrent or settings.max_concurrent_requests
    semaphore = asyncio.Semaphore(limit)

    async def process(
        request: GenerationRequest,
    ) -> GenerationResponse:
        async with semaphore:
            return await service.generate(request)

    return await asyncio.gather(
        *(process(request) for request in requests)
    )

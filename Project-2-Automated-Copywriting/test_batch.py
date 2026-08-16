import asyncio

from app.models.schemas import GenerationRequest, Platform, Tone
from app.services.batch_pipeline import generate_batch


async def main():
    requests = [
        GenerationRequest(
            product_name="Smart Water Bottle",
            product_description="A reusable water bottle that tracks daily water intake and helps users stay hydrated.",
            platform=Platform.INSTAGRAM,
            tone=Tone.FRIENDLY,
        ),
        GenerationRequest(
            product_name="Smart Water Bottle",
            product_description="A reusable water bottle that tracks daily water intake and helps users stay hydrated.",
            platform=Platform.LINKEDIN,
            tone=Tone.PROFESSIONAL,
        ),
        GenerationRequest(
            product_name="Smart Water Bottle",
            product_description="A reusable water bottle that tracks daily water intake and helps users stay hydrated.",
            platform=Platform.EMAIL,
            tone=Tone.PERSUASIVE,
        ),
    ]

    results = await generate_batch(requests)

    for result in results:
        print(f"\n--- {result.platform.value} / {result.tone.value} ---")
        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())

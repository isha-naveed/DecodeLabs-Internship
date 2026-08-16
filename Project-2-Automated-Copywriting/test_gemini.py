import asyncio

from app.clients.llm_client import GeminiClient


async def main():
    client = GeminiClient()

    response = await client.generate(
        prompt="Write one short marketing sentence for a smart water bottle.",
        temperature=0.7,
        top_p=0.9,
    )

    print("\nGemini response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
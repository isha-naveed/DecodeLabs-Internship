from google import genai

from app.config import settings


class GeminiClient:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        interaction = await self.client.aio.interactions.create(
            model=self.model,
            input=prompt,
            generation_config={
                "temperature": temperature,
                "top_p": top_p,
            },
        )

        if not interaction.output_text:
            raise RuntimeError("Gemini returned an empty response.")

        return interaction.output_text.strip()

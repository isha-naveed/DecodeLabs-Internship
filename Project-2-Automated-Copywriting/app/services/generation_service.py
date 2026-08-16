import json

from app.clients.llm_client import GeminiClient
from app.models.schemas import (
    EmailOutput,
    GenerationRequest,
    GenerationResponse,
    SocialMediaOutput,
)
from app.services.prompt_compiler import compile_prompt
from app.services.retry import retry_async


class GenerationService:
    def __init__(self) -> None:
        self.llm_client = GeminiClient()

    async def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        prompt = compile_prompt(request)

        raw_output = await retry_async(
            lambda: self.llm_client.generate(
                prompt=prompt,
                temperature=request.temperature,
                top_p=request.top_p,
            )
        )

        output = self._parse_output(
            request=request,
            raw_output=raw_output,
        )

        return GenerationResponse(
            platform=request.platform,
            tone=request.tone,
            output=output,
        )

    @staticmethod
    def _parse_output(
        request: GenerationRequest,
        raw_output: str,
    ) -> EmailOutput | SocialMediaOutput:
        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned invalid JSON."
            ) from exc

        if request.platform.value == "Email":
            try:
                return EmailOutput(
                    subject=data["subject"],
                    body=data["body"],
                )
            except (KeyError, TypeError) as exc:
                raise RuntimeError(
                    "Gemini returned an invalid email structure."
                ) from exc

        try:
            return SocialMediaOutput(
                content=data["content"],
                hashtags=data.get("hashtags", []),
            )
        except (KeyError, TypeError) as exc:
            raise RuntimeError(
                "Gemini returned an invalid social media structure."
            ) from exc

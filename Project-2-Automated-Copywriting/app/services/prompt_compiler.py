from app.prompts.master_template import MASTER_PROMPT
from app.prompts.platform_rules import PLATFORM_RULES
from app.models.schemas import GenerationRequest


def compile_prompt(request: GenerationRequest) -> str:
    platform = request.platform.value
    tone = request.tone.value

    platform_rules = PLATFORM_RULES[platform]

    return MASTER_PROMPT.format(
        product_name=request.product_name,
        product_description=request.product_description,
        platform=platform,
        tone=tone,
        platform_rules=platform_rules,
        temperature=request.temperature,
        top_p=request.top_p,
    )
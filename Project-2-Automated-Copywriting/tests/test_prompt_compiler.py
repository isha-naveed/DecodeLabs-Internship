from app.models.schemas import GenerationRequest, Platform, Tone
from app.services.prompt_compiler import compile_prompt


def test_prompt_contains_request_data():
    request = GenerationRequest(
        product_name="Smart Water Bottle",
        product_description="Tracks daily water intake.",
        platform=Platform.INSTAGRAM,
        tone=Tone.FRIENDLY,
    )

    prompt = compile_prompt(request)

    assert "Smart Water Bottle" in prompt
    assert "Tracks daily water intake." in prompt
    assert "Instagram" in prompt
    assert "Friendly" in prompt
    assert "Temperature: 0.7" in prompt
    assert "Top_P: 0.9" in prompt

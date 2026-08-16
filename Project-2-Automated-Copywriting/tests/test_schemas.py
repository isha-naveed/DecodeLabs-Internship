import pytest
from pydantic import ValidationError

from app.models.schemas import GenerationRequest, Platform, Tone


def test_valid_generation_request():
    request = GenerationRequest(
        product_name="Smart Water Bottle",
        product_description="Tracks daily water intake.",
        platform=Platform.INSTAGRAM,
        tone=Tone.FRIENDLY,
    )

    assert request.product_name == "Smart Water Bottle"
    assert request.platform == Platform.INSTAGRAM
    assert request.temperature == 0.7
    assert request.top_p == 0.9


def test_empty_product_name_rejected():
    with pytest.raises(ValidationError):
        GenerationRequest(
            product_name="   ",
            product_description="Tracks daily water intake.",
            platform=Platform.INSTAGRAM,
            tone=Tone.FRIENDLY,
        )


def test_invalid_temperature_rejected():
    with pytest.raises(ValidationError):
        GenerationRequest(
            product_name="Smart Water Bottle",
            product_description="Tracks daily water intake.",
            platform=Platform.INSTAGRAM,
            tone=Tone.FRIENDLY,
            temperature=3.0,
        )

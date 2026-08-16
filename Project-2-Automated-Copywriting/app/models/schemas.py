from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Platform(str, Enum):
    LINKEDIN = "LinkedIn"
    INSTAGRAM = "Instagram"
    EMAIL = "Email"


class Tone(str, Enum):
    PROFESSIONAL = "Professional"
    FRIENDLY = "Friendly"
    WITTY = "Witty"
    PERSUASIVE = "Persuasive"
    CASUAL = "Casual"
    LUXURY = "Luxury"
    INSPIRATIONAL = "Inspirational"


class GenerationRequest(BaseModel):
    product_name: str = Field(min_length=1, max_length=200)
    product_description: str = Field(min_length=1, max_length=3000)
    platform: Platform
    tone: Tone
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, gt=0.0, le=1.0)

    @field_validator("product_name", "product_description")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty.")

        return value


class EmailOutput(BaseModel):
    subject: str
    body: str


class SocialMediaOutput(BaseModel):
    content: str
    hashtags: list[str] = Field(default_factory=list)


class GenerationResponse(BaseModel):
    platform: Platform
    tone: Tone
    output: EmailOutput | SocialMediaOutput
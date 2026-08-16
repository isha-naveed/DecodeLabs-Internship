from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Automated Copywriting & Tone Transformer"
    app_version: str = "1.0.0"

    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"

    max_concurrent_requests: int = 3
    request_timeout: float = 60.0

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
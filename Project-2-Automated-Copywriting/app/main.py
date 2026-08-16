from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Automated Copywriting & Tone Transformer",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

from fastapi import FastAPI

from app.api.chat import router as chat_router

app = FastAPI(
    title="AI Chatbot API",
    version="1.0.0",
    description="Production-ready AI Chatbot Backend",
)

app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "AI Chatbot API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
from fastapi import FastAPI

app = FastAPI(
    title="AI Chatbot API",
    version="1.0.0",
    description="Production-ready AI Chatbot Backend"
)


@app.get("/")
def root():
    return {"message": "AI Chatbot API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
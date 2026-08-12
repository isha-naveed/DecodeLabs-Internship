from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.database.connection import create_tables


app = FastAPI(
    title="AI Chatbot API",
    version="1.0.0",
    description="Custom AI Chatbot with Memory",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    create_tables()


app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "AI Chatbot API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
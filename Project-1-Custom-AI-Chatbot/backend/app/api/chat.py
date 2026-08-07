from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.memory import ConversationMemory

router = APIRouter(prefix="/chat", tags=["Chat"])

chat_service = ChatService()
memory = ConversationMemory()


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = chat_service.send_message(
        request.message,
        memory,
    )

    return ChatResponse(response=response)
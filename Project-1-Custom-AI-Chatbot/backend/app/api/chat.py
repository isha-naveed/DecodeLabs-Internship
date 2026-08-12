from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.database.models import User
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.memory import ConversationMemory

router = APIRouter(prefix="/chat", tags=["Chat"])

chat_service = ChatService()

# One in-memory conversation per authenticated user.
# Memory is intentionally session-based and not stored in the database.
user_memories: dict[int, ConversationMemory] = {}


def get_user_memory(user_id: int) -> ConversationMemory:
    if user_id not in user_memories:
        user_memories[user_id] = ConversationMemory()

    return user_memories[user_id]


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ChatRepository(db)

    chat_record = repository.create_chat(
        user_id=current_user.id,
    )

    memory = get_user_memory(current_user.id)

    try:
        response = chat_service.send_message(
            request.message,
            memory,
        )
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again.",
        )

    repository.add_message(
        chat_id=chat_record.id,
        role="user",
        content=request.message,
    )

    repository.add_message(
        chat_id=chat_record.id,
        role="assistant",
        content=response,
    )

    return ChatResponse(response=response)


@router.post("/clear")
def clear_chat(
    current_user: User = Depends(get_current_user),
):
    user_memories.pop(current_user.id, None)

    return {
        "message": "Conversation memory cleared successfully."
    }

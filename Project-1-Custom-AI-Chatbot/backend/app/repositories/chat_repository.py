from sqlalchemy.orm import Session

from app.database.models import Chat, Message


class ChatRepository:
    """Handles database operations for chats and messages."""

    def __init__(self, db: Session):
        self.db = db

    def create_chat(
        self,
        user_id: int,
        title: str = "New Chat",
    ) -> Chat:
        chat = Chat(
            user_id=user_id,
            title=title,
        )

        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)

        return chat

    def add_message(
        self,
        chat_id: int,
        role: str,
        content: str,
    ) -> Message:
        message = Message(
            chat_id=chat_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_chat(
        self,
        chat_id: int,
        user_id: int,
    ) -> Chat | None:
        return (
            self.db.query(Chat)
            .filter(
                Chat.id == chat_id,
                Chat.user_id == user_id,
            )
            .first()
        )

    def get_messages(
        self,
        chat_id: int,
    ) -> list[Message]:
        return (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at)
            .all()
        )

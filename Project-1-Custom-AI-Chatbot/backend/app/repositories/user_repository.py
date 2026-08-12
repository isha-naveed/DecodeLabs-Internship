from sqlalchemy.orm import Session

from app.database.models import User


class UserRepository:
    """Handles database operations for users."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

    def get_by_id(self, user_id: int) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create_user(self, username: str, email: str, password_hash: str):
        user = User(
            username=username,
            email=email,
            hashed_password=password_hash,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
    
        return user
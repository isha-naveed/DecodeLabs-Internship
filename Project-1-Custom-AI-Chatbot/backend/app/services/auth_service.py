from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository


class AuthService:
    """Handles user registration and authentication."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def signup(self, username: str, email: str, password: str):
        password_hash = hash_password(password)

        return self.user_repository.create_user(
            username=username,
            email=email,
            password_hash=password_hash,
        )

    def login(self, username: str, password: str) -> str:
        user = self.user_repository.get_by_username(username)

        if not user or not verify_password(
            password,
            user.hashed_password,
        ):
            raise ValueError("Invalid username or password.")

        return create_access_token(
            {"sub": str(user.id)}
        )
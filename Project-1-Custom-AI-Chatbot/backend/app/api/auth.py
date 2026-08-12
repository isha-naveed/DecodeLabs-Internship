from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.database.connection import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse
from app.services.auth_service import AuthService

# from app.api.chat import user_memories
# from app.core.dependencies import get_current_user
# from app.database.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repository = UserRepository(db)
    return AuthService(repository)


@router.post("/signup", status_code=201)
def signup(
    request: SignupRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        service.signup(
        request.username,
        request.email,
        request.password,
        )
        return {"message": "User created successfully."}
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        token = service.login(
            request.username,
            request.password,
        )

        return TokenResponse(access_token=token)

    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        ) from exc


# @router.post("/logout")
# def logout(
#     current_user: User = Depends(get_current_user),
# ):
#     user_memories.pop(current_user.id, None)

#     return {
#         "message": "Logged out successfully."
#     }
from app.database import get_db
from app.models.user_entry import UserEntry
from app.repositories.users.user_repository import UserRepository
from app.schemas.user import (
    CreateUser,
    CreateUserResponse,
)
from app.services.users.user_service import UserService
from exceptions.repository_exceptions import RepositoryError, UserAlreadyExist
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse
)
async def create_user(
    create_user: CreateUser,
    db: Session = Depends(get_db),  # noqa: B008
) -> UserEntry:
    user_service = UserService(UserRepository(db))
    try:
        return await user_service.add(create_user)
    except UserAlreadyExist as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    except RepositoryError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )

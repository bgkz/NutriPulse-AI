from app.database import get_db
from app.models.user_entry import UserEntry
from app.repositories.users.user_repository import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.users.user_service import UserService
from exceptions.repository_exceptions import RepositoryError
from exceptions.service_exceptions import InvalidPasswordError, UserNotFoundError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/login")


@router.post("/", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login(
    user_login_request: LoginRequest,
    db: Session = Depends(get_db),  # noqa: B008
) -> UserEntry:
    user_service = UserService(UserRepository(db=db))
    try:
        return await user_service.find(user_login_request)

    except (InvalidPasswordError, UserNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username or Password",
        )
    except RepositoryError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )

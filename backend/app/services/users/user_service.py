from app.models.user_entry import UserEntry
from app.repositories.users.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.schemas.user import CreateUser
from exceptions.service_exceptions import InvalidPasswordError, UserNotFoundError
from pwdlib import PasswordHash


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def add(self, user: CreateUser) -> UserEntry:
        password_hash = PasswordHash.recommended()
        hashed_password = password_hash.hash(user.password)
        user.password = hashed_password

        return await self.user_repo.add(
            UserEntry(username=user.username, password_hash=user.password)
        )

    async def find(self, user_login_request: LoginRequest) -> UserEntry:
        user_found = await self.user_repo.find_user_by_name(user_login_request.username)
        if not user_found:
            raise UserNotFoundError(f"User {user_login_request.username} not found")
        password_hash = PasswordHash.recommended()
        is_valid = password_hash.verify(
            user_login_request.password,
            user_found.password_hash,
        )
        if not is_valid:
            raise InvalidPasswordError(
                f"Password for user {user_login_request.username} is invalid"
            )
        return user_found

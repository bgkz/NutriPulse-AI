from app.models.user_entry import UserEntry
from app.repositories.users.user_repository import UserRepository
from app.schemas.user import CreateUser
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

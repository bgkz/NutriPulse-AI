from app.models.user_entry import UserEntry
from exceptions.repository_exceptions import RepositoryError, UserAlreadyExist
from sqlalchemy.exc import IntegrityError, PendingRollbackError, SQLAlchemyError
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def add(self, user: UserEntry) -> UserEntry:
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError as error:
            self.db.rollback()
            raise UserAlreadyExist(f"User: {user.username} already exist") from error
        except SQLAlchemyError as error:
            self.db.rollback()
            raise RepositoryError("Repository operation failed") from error
        except PendingRollbackError as exc:
            self.db.rollback()
            raise RepositoryError("Database session was in invalid state") from exc

from uuid import UUID

from app.models.message_entry import MessageEntry
from exceptions.repository_exceptions import MessageAlreadyExist, RepositoryError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class MessageRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, message: MessageEntry) -> MessageEntry:
        try:
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)
            return message
        except IntegrityError as error:
            self.db.rollback()
            raise MessageAlreadyExist("Message already exist") from error
        except SQLAlchemyError as error:
            self.db.rollback()
            raise RepositoryError("Adding Message operation failed: ", error) from error

    def get_messages_by_conversation_id(
        self, conversation_id: UUID
    ) -> list[MessageEntry]:

        stmt = (
            select(MessageEntry)
            .where(MessageEntry.conversation_id == conversation_id)
            .order_by((MessageEntry.created_at).asc())
        )

        return self.db.execute(statement=stmt).scalars().all()

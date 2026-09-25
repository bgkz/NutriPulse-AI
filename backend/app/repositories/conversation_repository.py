from uuid import UUID

from app.models.conversation_entry import ConversationEntry
from exceptions.repository_exceptions import ConversationAlreadyExist, RepositoryError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class ConversationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def update_title(
        self, conversation: ConversationEntry, target_title: str
    ) -> ConversationEntry:
        try:
            conversation.title = target_title
            self.db.commit()
            self.db.refresh(conversation)
            return conversation
        except SQLAlchemyError as error:
            self.db.rollback()
            raise RepositoryError(
                "Update Conversation Title failed: ", error
            ) from error

    def get(self, conversation_id: UUID) -> ConversationEntry | None:
        stmt = select(ConversationEntry).where(ConversationEntry.id == conversation_id)
        return self.db.execute(statement=stmt).scalar_one_or_none()

    def add(self, conversation: ConversationEntry) -> ConversationEntry:
        try:
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
            return conversation
        except IntegrityError as error:
            self.db.rollback()
            raise ConversationAlreadyExist("Conversation already exist") from error
        except SQLAlchemyError as error:
            self.db.rollback()
            raise RepositoryError(
                "Adding Conversation operation failed: ", error
            ) from error

    def get_conversations_by_user(self, user_id: UUID) -> list[ConversationEntry]:
        stmt = (
            select(ConversationEntry)
            .where(ConversationEntry.user_id == user_id)
            .order_by((ConversationEntry.created_at).asc())
        )
        return self.db.execute(statement=stmt).scalars().all()

from uuid import UUID

from app.models.message_entry import MessageEntry
from sqlalchemy import select
from sqlalchemy.orm import Session


class MessageRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_messages_by_conversation_id(
        self, conversation_id: UUID
    ) -> list[MessageEntry]:

        stmt = (
            select(MessageEntry)
            .where(MessageEntry.conversation_id == conversation_id)
            .order_by((MessageEntry.created_at).desc())
        )

        return self.db.execute(statement=stmt).scalars().all()

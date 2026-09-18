from uuid import UUID

from app.models.conversation_entry import ConversationEntry
from sqlalchemy import select
from sqlalchemy.orm import Session


class ConversationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_conversations_by_user(self, user_id: UUID) -> list[ConversationEntry]:
        stmt = (
            select(ConversationEntry)
            .where(ConversationEntry.user_id == user_id)
            .order_by((ConversationEntry.created_at).asc())
        )
        return self.db.execute(statement=stmt).scalars().all()

from app.models.conversation_entry import ConversationEntry
from sqlalchemy.orm import Session


class ChatRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_conversations_by_user_id(
        self, user_id: str
    ) -> list[ConversationEntry] | None:
        return None

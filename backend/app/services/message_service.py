from uuid import UUID

from app.models.message_entry import MessageEntry
from app.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, message_repo: MessageRepository) -> None:
        self.message_repo = message_repo

    def get_messages_by_conversation_id(
        self, conversation_id: UUID
    ) -> list[MessageEntry]:
        return self.message_repo.get_messages_by_conversation_id(conversation_id)

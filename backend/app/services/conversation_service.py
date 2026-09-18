from uuid import UUID

from app.models.conversation_entry import ConversationEntry
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    def __init__(self, conversation_repo: ConversationRepository) -> None:
        self.conversation_repo = conversation_repo

    def get_conversations_by_user(self, user_id: UUID) -> list[ConversationEntry]:
        return self.conversation_repo.get_conversations_by_user(user_id)

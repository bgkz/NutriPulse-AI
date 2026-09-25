from uuid import UUID

from app.models.conversation_entry import ConversationEntry
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    def __init__(self, conversation_repo: ConversationRepository) -> None:
        self.conversation_repo = conversation_repo

    def update_title(
        self, conversation: ConversationEntry, target_title: str
    ) -> ConversationEntry:

        return self.conversation_repo.update_title(
            conversation=conversation, target_title=target_title
        )

    def get_conversation(self, conversation_id: UUID) -> ConversationEntry | None:
        return self.conversation_repo.get(conversation_id)

    def create_conversation(self, user_id: UUID) -> ConversationEntry:
        conversation = ConversationEntry(user_id=user_id)
        return self.conversation_repo.add(conversation)

    def get_conversations_by_user(self, user_id: UUID) -> list[ConversationEntry]:
        return self.conversation_repo.get_conversations_by_user(user_id)

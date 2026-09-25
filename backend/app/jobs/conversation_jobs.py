from uuid import UUID

from app.database import SessionLocal
from app.models.conversation_entry import ConversationEntry
from app.repositories.conversation_repository import ConversationRepository
from app.services.conversation_service import ConversationService


def get_conversation(conversation_id: UUID) -> ConversationEntry | None:
    with SessionLocal() as db:
        conversation_service = ConversationService(ConversationRepository(db=db))
        return conversation_service.get_conversation(conversation_id=conversation_id)


def update_conversation_title(conversation_id: UUID, target_title: str):
    with SessionLocal() as db:
        conversation_service = ConversationService(ConversationRepository(db=db))
        conversation = conversation_service.get_conversation(conversation_id)
        if conversation is None:
            raise ValueError(f"Conversation {conversation_id} not found")
        return conversation_service.update_title(
            conversation=conversation, target_title=target_title
        )

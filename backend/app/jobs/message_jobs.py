from uuid import UUID

from app.database import SessionLocal
from app.models.conversation_entry import ConversationEntry
from app.models.message_entry import MessageEntry, RoleType
from app.repositories.message_repository import MessageRepository
from app.services.message_service import MessageService
from rq.job import Job


def get_messages_by_conversation_id(conversation_id: UUID) -> list[MessageEntry]:
    with SessionLocal() as db:
        message_service = MessageService(MessageRepository(db=db))
        return message_service.get_messages_by_conversation_id(
            conversation_id=conversation_id
        )


def add_message_to_db(
    message: str, conversation_id: UUID, role: RoleType
) -> MessageEntry:
    with SessionLocal() as db:
        message_service = MessageService(MessageRepository(db=db))
        return message_service.add_message(
            message=message, conversation_id=conversation_id, role=role
        )

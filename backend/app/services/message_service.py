from uuid import UUID

from app.models.message_entry import MessageEntry, RoleType
from app.repositories.message_repository import MessageRepository
from app.schemas.chat import SendMessageRequest


class MessageService:
    def __init__(self, message_repo: MessageRepository) -> None:
        self.message_repo = message_repo

    def create_message(self, send_message_request: SendMessageRequest) -> MessageEntry:
        message_entry = MessageEntry(
            conversation_id=send_message_request.conversation_id,
            role=RoleType(send_message_request.role.casefold()),
            content=send_message_request.content,
        )
        
        return self.message_repo.add(message_entry)

    def get_messages_by_conversation_id(
        self, conversation_id: UUID
    ) -> list[MessageEntry]:
        return self.message_repo.get_messages_by_conversation_id(conversation_id)

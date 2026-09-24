from uuid import UUID

from app.models.conversation_entry import ConversationEntry
from app.models.message_entry import MessageEntry
from app.repositories.chat.chat_repository import ChatRepository
from app.schemas.chat import SendMessageRequest
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService


class ChatService:
    def __init__(
        self, conversation_service: ConversationService, message_service: MessageService
    ):
        self.conversation_service = conversation_service
        self.message_service = message_service

    def get_conversation(self, conversation_id: UUID) -> ConversationEntry | None:
        return self.conversation_service.get_conversation(conversation_id)

    def create_message(self, send_message_request: SendMessageRequest) -> MessageEntry:
        return self.message_service.create_message(send_message_request)

    def create_conversation(self, user_id: UUID) -> ConversationEntry:
        return self.conversation_service.create_conversation(user_id)

    def get_conversations_by_user_id(
        self, user_id: str
    ) -> list[ConversationEntry] | None:
        return self.chat_repo.get_conversations_by_user_id(user_id)

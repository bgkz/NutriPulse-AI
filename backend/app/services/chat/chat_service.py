from app.models.conversation_entry import ConversationEntry
from app.repositories.chat.chat_repository import ChatRepository


class ChatService:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repo = chat_repository

    def get_conversations_by_user_id(
        self, user_id: str
    ) -> list[ConversationEntry] | None:
        return self.chat_repo.get_conversations_by_user_id(user_id)

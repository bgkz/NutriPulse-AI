import uuid

from app.schemas.conversation import ConversationResponse
from app.schemas.message import MessageResponse
from pydantic import BaseModel


class SendMessageRequest(BaseModel):
    conversation_id: uuid.UUID | None
    role: str
    content: str


class SendMessageResponse(BaseModel):
    conversation: ConversationResponse
    message: MessageResponse
    job: str

    model_config = {"from_attributes": True}

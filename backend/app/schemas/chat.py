import datetime
import uuid

from pydantic import BaseModel


class SendMessageRequest(BaseModel):
    conversation_id: uuid.UUID | None
    role: str
    content: str

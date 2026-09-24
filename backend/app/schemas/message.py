import datetime
import uuid

from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    created_at: datetime.datetime

    model_config = {"from_attributes": True}

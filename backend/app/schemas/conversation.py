import datetime
import uuid

from pydantic import BaseModel


class ConversationResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str | None
    created_at: datetime.datetime

    model_config = {"from_attributes": True}

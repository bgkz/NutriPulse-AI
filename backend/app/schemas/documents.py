from uuid import UUID

from pydantic import BaseModel


class UrlImportRequest(BaseModel):
    url: str
    conversation_id: UUID | None

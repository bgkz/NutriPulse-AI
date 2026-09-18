from pydantic import BaseModel


class ChatRequest(BaseModel):
    role: str
    content: str

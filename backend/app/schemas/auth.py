import uuid

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    id: uuid.UUID
    username: str
    password_hash: str

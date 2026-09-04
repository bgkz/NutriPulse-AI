import uuid

from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    password: str


class CreateUserResponse(BaseModel):
    id: uuid.UUID
    username: str
    password_hash: str

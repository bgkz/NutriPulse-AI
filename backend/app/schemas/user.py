import uuid

from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    username: str
    password: str = Field(min_length=8, max_length=128)


class CreateUserResponse(BaseModel):
    id: uuid.UUID
    username: str
    password_hash: str

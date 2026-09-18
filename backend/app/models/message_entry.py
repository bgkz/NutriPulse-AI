import datetime
import uuid
from enum import Enum

import sqlalchemy as sa
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class RoleType(Enum):
    USER = "user"
    ASSISTANT = "assistant"


class MessageEntry(Base):
    __tablename__ = "messages"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("conversations.id"),
        index=True,
    )

    role: Mapped[RoleType] = mapped_column(nullable=False)

    content: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        server_default=sa.func.now(),
    )

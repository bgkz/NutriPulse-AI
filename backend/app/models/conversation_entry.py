import datetime
import uuid

import sqlalchemy as sa
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class ConversationEntry(Base):
    __tablename__ = "conversations"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    title: Mapped[str | None] = mapped_column(unique=True)

    created_at: Mapped[datetime.date] = mapped_column(
        default=datetime.date.today,
        server_default=sa.func.current_date(),
    )

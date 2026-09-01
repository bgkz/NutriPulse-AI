import uuid

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserEntry(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    username: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )

    password_hash: Mapped[str]

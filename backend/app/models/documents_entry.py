import datetime
import uuid
from enum import Enum

import sqlalchemy as sa
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class StatusType(Enum):
    FAILED = "Failed"
    PROCESSING = "Processing"
    SUCCESS = "Success"


class DocumentsEntry(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)

    url: Mapped[str]

    imported_at: Mapped[datetime.date] = mapped_column(
        default=datetime.date.today,
        server_default=sa.func.current_date(),
    )

    processing_status: Mapped[StatusType] = mapped_column(
        default=StatusType.PROCESSING,
        server_default="PROCESSING",
    )

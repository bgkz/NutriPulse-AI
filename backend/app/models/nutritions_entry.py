import datetime
import uuid

from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class NutritionsEntry(Base):
    __tablename__ = "nutritions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id"), index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    date: Mapped[datetime.date | None] = mapped_column(unique=True)

    calories: Mapped[int | None]
    protein: Mapped[int | None]
    carbs: Mapped[int | None]
    fat: Mapped[int | None]
    bodyweight_kg: Mapped[float | None]
    steps: Mapped[int | None]
    notes: Mapped[str | None]

import uuid
from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ExerciseNotesEntry(Base):
    __tablename__ = "exercise_notes"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    note_date: Mapped[date] = mapped_column(
        ForeignKey("nutritions.nutrition_date"),
        unique=True,
    )
    note: Mapped[str]

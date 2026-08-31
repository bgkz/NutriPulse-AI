import uuid
from datetime import date
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ExerciseTypeEntry(Base):
    __tablename__ = "exercise_types"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    exercise_name: Mapped[str] = mapped_column(unique=True)
    exercise_name_normalized: Mapped[str] = mapped_column(unique=True)

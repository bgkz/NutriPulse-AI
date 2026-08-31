import uuid
from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ExerciseSetsEntry(Base):
    __tablename__ = "exercise_sets"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    exercise_date: Mapped[date] = mapped_column(
        ForeignKey("nutritions.nutrition_date"), index=True
    )
    exercise_name: Mapped[str] = mapped_column(index=True)

    weight: Mapped[float]
    repetitions: Mapped[int]

    reps_in_reserve: Mapped[int | None]

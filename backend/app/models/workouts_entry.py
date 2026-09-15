import datetime
import uuid

from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class WorkoutsEntry(Base):
    __tablename__ = "workouts"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id"), index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    date: Mapped[datetime.date | None] = mapped_column(index=True)

    exercise: Mapped[str | None]
    weight_kg: Mapped[float | None]
    reps_in_set_one: Mapped[int | None]
    reps_in_set_two: Mapped[int | None]
    reps_in_set_three: Mapped[int | None]
    rest_in_reserve_min: Mapped[int | None]
    rest_in_reserve_max: Mapped[int | None]

import uuid
from datetime import date

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class NutritionEntry(Base):
    __tablename__ = "nutritions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    nutrition_date: Mapped[date] = mapped_column(
        unique=True,
        index=True,
    )

    training: Mapped[str | None]
    steps: Mapped[int | None]

    calories: Mapped[int | None]
    protein: Mapped[int | None]
    fat: Mapped[int | None]
    carbs: Mapped[int | None]

    weight: Mapped[float | None]
    notes: Mapped[str | None]

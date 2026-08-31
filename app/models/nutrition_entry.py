from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class NutritionEntry(Base):
    __tablename__ = "nutritions"

    id: Mapped[int] = mapped_column(primary_key=True)

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

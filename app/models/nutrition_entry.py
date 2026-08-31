import uuid
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


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

    def __repr__(self) -> str:
        return (
            f"NutritionEntry("
            f"date={self.nutrition_date}, "
            f"training={self.training!r}, "
            f"steps={self.steps}, "
            f"calories={self.calories}, "
            f"protein={self.protein}, "
            f"fat={self.fat}, "
            f"carbs={self.carbs}, "
            f"weight={self.weight}, "
            f"notes={self.notes!r}"
            f")"
        )

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.nutrition_entry import NutritionEntry


class NutritionRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, nutrition_entry: NutritionEntry) -> NutritionEntry:
        try:
            self.db.add(nutrition_entry)
            self.db.commit()
            self.db.refresh(nutrition_entry)
            return nutrition_entry
        except IntegrityError as error:
            print(error)

        except SQLAlchemyError as error:
            print(error)

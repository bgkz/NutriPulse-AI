from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.nutrition_entry import NutritionEntry
from exceptions.repository_exceptions import NutritionEntryAlreadyExist, RepositoryError


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
            self.db.rollback()
            raise NutritionEntryAlreadyExist(
                "Adding Nutrition failed: Either nutrition_date already exist oder some foreignkey issues"
            ) from error

        except SQLAlchemyError as error:
            self.db.rollback()
            raise RepositoryError("Adding Nutrition operation failed") from error

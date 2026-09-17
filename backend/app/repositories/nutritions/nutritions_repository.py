from app.models.nutritions_entry import NutritionsEntry
from exceptions.repository_exceptions import NutritionEntryAlreadyExist, RepositoryError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class NutritionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, nutrition_entry: NutritionsEntry) -> NutritionsEntry:
        try:
            self.db.add(nutrition_entry)
            self.db.commit()
            self.db.refresh(nutrition_entry)
            return nutrition_entry
        except IntegrityError as error:
            self.db.rollback()
            raise NutritionEntryAlreadyExist("Nutrition already exist") from error
        except SQLAlchemyError as error:
            self.db.rollback()
            raise RepositoryError(
                "Adding nutrition entry operation failed: ", error
            ) from error

from app.models.exercise_sets_entry import ExerciseSetsEntry
from exceptions.repository_exceptions import (
    ExerciseSetEntryAlreadyExist,
    RepositoryError,
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class ExerciseSetsRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, exercise_set_entry: ExerciseSetsEntry) -> ExerciseSetsEntry:
        try:
            self.db.add(exercise_set_entry)
            self.db.commit()
            self.db.refresh(exercise_set_entry)
            return exercise_set_entry
        except IntegrityError as error:
            self.db.rollback()
            raise ExerciseSetEntryAlreadyExist(
                "Adding Exercise_Set failed: Either exercise_date already exist oder some foreignkey issues"
            ) from error
        except SQLAlchemyError as error:
            self.db.rollback()
            raise RepositoryError("Adding Exercise operation failed") from error

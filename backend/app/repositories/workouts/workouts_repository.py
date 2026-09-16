from app.models.workouts_entry import WorkoutsEntry
from exceptions.repository_exceptions import RepositoryError, WorkoutsEntryAlreadyExist
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class WorkoutsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, workouts_entry: WorkoutsEntry) -> WorkoutsEntry:
        try:
            self.db.add(workouts_entry)
            self.db.commit()
            self.db.refresh(workouts_entry)
            return workouts_entry
        except IntegrityError as error:
            self.db.rollback()
            raise WorkoutsEntryAlreadyExist("Workout already exist") from error
        except SQLAlchemyError as error:
            self.db.rollback()
            raise RepositoryError("Adding Workout operation failed: ", error) from error

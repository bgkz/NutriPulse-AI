from app.models.workouts_entry import WorkoutsEntry
from app.repositories.workouts.workouts_repository import WorkoutsRepository


class WorkoutsService:
    def __init__(self, workouts_repo: WorkoutsRepository) -> WorkoutsEntry:
        self.workouts_repo = workouts_repo

    
    def add(self, workouts_entry: WorkoutsEntry) -> WorkoutsEntry:
        return self.workouts_repo.add(workouts_entry)
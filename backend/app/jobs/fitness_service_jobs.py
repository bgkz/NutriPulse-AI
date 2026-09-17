from app.database import SessionLocal
from app.models.documents_entry import DocumentsEntry
from app.models.nutritions_entry import NutritionsEntry
from app.models.user_entry import UserEntry
from app.models.workouts_entry import WorkoutsEntry
from app.queue import redis_connection
from app.repositories.nutritions.nutritions_repository import NutritionRepository
from app.repositories.workouts.workouts_repository import WorkoutsRepository
from app.schemas.fitness import FitnessEntries
from app.services.nutritions.nutritions_service import NutritionsService
from app.services.workouts.workouts_service import WorkoutsService
from rq.job import Job


def save_parsed_fitness_entries_in_db(
    parse_data_job_id: str,
    save_document_job_id: str,
):

    parsed_data = Job.fetch(parse_data_job_id, connection=redis_connection).result
    document: DocumentsEntry = Job.fetch(
        save_document_job_id, connection=redis_connection
    ).result

    fitness_entries = FitnessEntries.model_validate(parsed_data)
    with SessionLocal() as db:
        nutrition_service = NutritionsService(NutritionRepository(db=db))
        workout_service = WorkoutsService(WorkoutsRepository(db=db))
        for nutrition_data in fitness_entries.nutrition:
            nutrition_entry = NutritionsEntry(
                **nutrition_data.model_dump(),
                document_id=document.id,
                user_id=document.user_id,
            )
            nutrition_service.add(nutrition_entry)

        for workout_data in fitness_entries.workouts:
            workouts_entry = WorkoutsEntry(
                **workout_data.model_dump(),
                document_id=document.id,
                user_id=document.user_id,
            )
            workout_service.add(workouts_entry)

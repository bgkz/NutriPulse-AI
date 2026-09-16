from app.core.security import decode_access_token
from app.database import get_db
from app.jobs.llm_service_jobs import parse_data_with_llm
from app.models.documents_entry import DocumentsEntry, StatusType
from app.models.nutritions_entry import NutritionsEntry
from app.models.workouts_entry import WorkoutsEntry
from app.queue import queue, redis_connection
from app.repositories.documents.documents_repository import DocumentsRepository
from app.repositories.nutritions.nutritions_repository import NutritionRepository
from app.repositories.workouts.workouts_repository import WorkoutsRepository
from app.schemas.documents import UrlImportRequest
from app.schemas.fitness import FitnessEntries
from app.services.documents.documents_service import DocumentsService
from app.services.google.google_service import GoogleService
from app.services.nutritions.nutritions_service import NutritionsService
from app.services.workouts.workouts_service import WorkoutsService
from exceptions.google_service_exceptions import (
    GoogleSheetsError,
    SpreadsheetNotFoundError,
)
from exceptions.repository_exceptions import (
    DocumentAlreadyExist,
    NutritionEntryAlreadyExist,
    RepositoryError,
    WorkoutsEntryAlreadyExist,
)
from exceptions.security_exceptions import InvalidAccessTokenError
from exceptions.service_exceptions import DocumentWithJobIDNotFound
from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    status,
)
from rq.job import Job
from sqlalchemy.orm import Session

router = APIRouter(prefix="/documents")


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def import_url(
    data: UrlImportRequest,
    authorization: str = Header(),
    db: Session = Depends(get_db),  # noqa: B008
):
    try:
        token = authorization.removeprefix("Bearer ")
        payload = decode_access_token(token)
        user_id = payload["sub"]

        google_service = GoogleService()
        sheets_data = google_service.load(data.url)
        job = queue.enqueue(parse_data_with_llm, sheets_data)

        document = DocumentsEntry(user_id=user_id, url=data.url, job_id=job.id)
        document_service = DocumentsService(DocumentsRepository(db=db))
        document_service.add(document)

        return {"job_id": job.id, "status": job.get_status()}

    except DocumentAlreadyExist as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    except InvalidAccessTokenError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
    except SpreadsheetNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except GoogleSheetsError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error))
    except RepositoryError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )


@router.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):  # noqa: B008
    try:
        job = Job.fetch(job_id, connection=redis_connection)

        if job.is_finished:
            documents_service = DocumentsService(DocumentsRepository(db=db))
            nutrition_service = NutritionsService(NutritionRepository(db=db))
            workout_service = WorkoutsService(WorkoutsRepository(db=db))
            doc_found = documents_service.find_document_by_job_id(job_id)

            fitness_entries = FitnessEntries.model_validate(job.result)

            for nutrition_data in fitness_entries.nutrition:
                nutrition_entry = NutritionsEntry(
                    **nutrition_data.model_dump(),
                    document_id=doc_found.id,
                    user_id=doc_found.user_id,
                )
                nutrition_service.add(nutrition_entry)

            for workout_data in fitness_entries.workouts:
                workouts_entry = WorkoutsEntry(
                    **workout_data.model_dump(),
                    document_id=doc_found.id,
                    user_id=doc_found.user_id,
                )
                workout_service.add(workouts_entry)

            doc_updated = documents_service.update_processing_status(
                doc_found, StatusType.SUCCESS
            )
            return {"status": job.get_status(), "result": job.result}
        if not job.is_finished:
            return {"status": job.get_status(), "result": None}

    except DocumentWithJobIDNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except NutritionEntryAlreadyExist as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    except WorkoutsEntryAlreadyExist as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
    except RepositoryError as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )

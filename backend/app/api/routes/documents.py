from app.core.security import decode_access_token
from app.database import get_db
from app.jobs.llm_service_jobs import parse_data_with_llm
from app.queue import queue, redis_connection
from app.schemas.documents import UrlImportRequest
from app.schemas.fitness import FitnessEntries
from app.services.google.google_service import GoogleService
from exceptions.google_service_exceptions import (
    GoogleSheetsError,
    SpreadsheetNotFoundError,
)
from exceptions.security_exceptions import InvalidAccessTokenError
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
        return {"job_id": job.id, "status": job.get_status()}

    except InvalidAccessTokenError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
    except SpreadsheetNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except GoogleSheetsError as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(error))


@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = Job.fetch(job_id, connection=redis_connection)

    if not job.is_finished:
        return {"status": job.get_status(), "result": None}

    fitness_entries = FitnessEntries.model_validate(job.result)

    print(f"Nutritions: {fitness_entries.nutrition}")
    print(f"Workout: {fitness_entries.workouts}")

    return {"status": job.get_status(), "result": job.result}

from app.core.security import decode_access_token
from app.database import get_db
from app.jobs.jobs import process_import
from app.queue import redis_connection
from app.schemas.documents import UrlImportRequest
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
def import_url(
    data: UrlImportRequest,
    authorization: str = Header(),
    db: Session = Depends(get_db),  # noqa: B008
):
    try:
        token = authorization.removeprefix("Bearer ")
        payload = decode_access_token(token)
        user_id = payload["sub"]

        job = process_import(data.url, user_id)

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

        print(job.get_status())

        if job.is_finished:
            return {"status": job.get_status(), "result": job.result}
        if job.is_failed:
            return {"status": "failed", "error": job.exc_info}
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

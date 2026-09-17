from app.core.security import decode_access_token
from app.jobs.jobs import process_import
from app.queue import redis_connection
from app.schemas.documents import UrlImportRequest
from exceptions.security_exceptions import InvalidAccessTokenError
from fastapi import (
    APIRouter,
    Header,
    HTTPException,
    status,
)
from rq.exceptions import NoSuchJobError
from rq.job import Job

router = APIRouter(prefix="/documents")


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def import_url(data: UrlImportRequest, authorization: str = Header()):
    try:
        token = authorization.removeprefix("Bearer ")
        payload = decode_access_token(token)
        user_id = payload["sub"]

        job = process_import(data.url, user_id)

        return {"job_id": job.id, "status": job.get_status()}

    except InvalidAccessTokenError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))


@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_connection)
        if job.is_finished:
            return {"status": job.get_status(), "result": job.result}
        if job.is_failed:
            return {"status": "failed", "error": job.exc_info}
        if not job.is_finished:
            return {"status": job.get_status(), "result": None}

    except NoSuchJobError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

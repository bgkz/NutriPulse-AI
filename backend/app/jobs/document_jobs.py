from typing import Any

from app.database import SessionLocal
from app.models.documents_entry import DocumentsEntry, StatusType
from app.models.nutritions_entry import NutritionsEntry
from app.models.user_entry import UserEntry
from app.queue import redis_connection
from app.repositories.documents.documents_repository import DocumentsRepository
from app.services.documents.documents_service import DocumentsService
from rq.job import Job


def save_document_in_db(user_id: Any, url: str) -> DocumentsEntry:

    with SessionLocal() as db:
        document_service = DocumentsService(DocumentsRepository(db=db))
        doc = DocumentsEntry(user_id=user_id, url=url)
        return document_service.add(doc)


def update_document_processing_status_to_success(
    added_document_job_id: str,
    parsed_data_job_id: str,
) -> dict[str, Any]:

    parsed_data = Job.fetch(parsed_data_job_id, connection=redis_connection).result
    if parsed_data is None:
        raise ValueError(f"LLM job {parsed_data_job_id} has no result")

    document: DocumentsEntry = Job.fetch(
        added_document_job_id, connection=redis_connection
    ).result

    with SessionLocal() as db:
        stored_document = db.get(DocumentsEntry, document.id)
        if stored_document is None:
            raise ValueError(f"Document {document.id} not found")
        document_service = DocumentsService(DocumentsRepository(db=db))
        document_service.update_processing_status(stored_document, StatusType.SUCCESS)

    return parsed_data

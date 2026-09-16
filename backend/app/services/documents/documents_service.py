from app.models.documents_entry import DocumentsEntry, StatusType
from app.repositories.documents.documents_repository import DocumentsRepository
from exceptions.service_exceptions import DocumentWithJobIDNotFound


class DocumentsService:
    def __init__(self, document_repo: DocumentsRepository) -> DocumentsRepository:
        self.document_repo = document_repo

    def add(self, document: DocumentsEntry) -> DocumentsEntry:
        return self.document_repo.add(document)

    def find_document_by_job_id(self, job_id: str) -> DocumentsEntry:
        doc_found = self.document_repo.find_document_by_job_id(job_id)
        if not doc_found:
            raise DocumentWithJobIDNotFound(f"document not found with job_id {job_id}")

        return doc_found

    def update_processing_status(
        self, document: DocumentsEntry, target_status: StatusType
    ) -> DocumentsEntry:
        if document.processing_status == target_status:
            raise ValueError("Status already changed")

        return self.document_repo.update_processing_status(document, target_status)

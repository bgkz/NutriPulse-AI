from app.models.documents_entry import DocumentsEntry, StatusType
from exceptions.repository_exceptions import DocumentAlreadyExist, RepositoryError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class DocumentsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, document: DocumentsEntry) -> DocumentsEntry:
        try:
            self.db.add(document)
            self.db.commit()
            self.db.refresh(document)
            return document
        except IntegrityError as error:
            self.db.rollback()
            raise DocumentAlreadyExist("document already exist") from error
        except SQLAlchemyError as error:
            self.db.rollback()
            raise RepositoryError("Adding document operation failed") from error

    def find_document_by_job_id(self, job_id: str) -> DocumentsEntry | None:
        stmt = select(DocumentsEntry).where(DocumentsEntry.job_id == job_id)
        result = self.db.execute(statement=stmt).scalar_one_or_none()
        return result

    def update_processing_status(
        self, document: DocumentsEntry, target_status: StatusType
    ) -> DocumentsEntry:
        try:
            document.processing_status = target_status
            self.db.commit()
            self.db.refresh(document)
            return document
        except SQLAlchemyError as error:
            self.db.rollback()
            raise RepositoryError("Update Processing Status failed: ", error) from error

import json
import logging
from uuid import UUID

from app.database import SessionLocal
from app.models.documents_entry import DocumentsEntry
from app.services.google.google_service import GoogleService
from sqlalchemy import select

READ_SHEET_TOOL = {
    "type": "function",
    "name": "read_sheet",
    "description": "Liest aktuelle Fitnessdaten aus einem verknüpften Google Sheet.",
    "parameters": {
        "type": "object",
        "properties": {
            "document_id": {
                "type": "string",
                "description": "ID eines verfügbaren Dokuments aus dem Kontext.",
            }
        },
        "required": ["document_id"],
        "additionalProperties": False,
    },
    "strict": True,
}


def get_user_documents(user_id: UUID) -> dict[str, str]:
    # Nur Dokumente des angemeldeten Nutzers stehen dem Tool zur Verfügung.
    with SessionLocal() as db:
        documents = db.scalars(
            select(DocumentsEntry).where(DocumentsEntry.user_id == user_id)
        ).all()
        return {str(document.id): document.url for document in documents}


def execute_sheet_tool(name: str, arguments: str, documents: dict[str, str]) -> dict:
    if name != "read_sheet":
        return {"error": "Unbekanntes Tool."}

    try:
        args = json.loads(arguments)
    except (ValueError, TypeError):
        return {"error": "Ungültige Tool-Argumente."}

    document_id = args.get("document_id") if isinstance(args, dict) else None
    if not isinstance(document_id, str) or document_id not in documents:
        return {"error": "Dokument nicht gefunden oder kein Zugriff."}

    try:
        data = GoogleService().load(documents[document_id])

        return {"document_id": document_id, "data": data}
    except Exception:
        logging.getLogger(__name__).exception("Sheet konnte nicht geladen werden")
        return {
            "error": "Sheet konnte nicht geladen werden. Bitte später erneut versuchen."
        }

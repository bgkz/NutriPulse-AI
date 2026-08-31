import gspread
from sqlalchemy.orm import Session

from app import database
from app.api.google_sheets_client import GoogleSheetsClient
from app.config import GOOGLE_SHEET_SPREADSHEET_ID
from app.factory.repository_factory import RepositoryFactory
from app.factory.worksheet_processor_factory import (
    WorksheetProcessorFactory,
)


class GoogleSheetsImportService:
    def __init__(self, google_sheets_client: GoogleSheetsClient, db: Session):
        self.client = google_sheets_client
        self.db = db

    def import_all_worksheets(self, spreadsheet_id: str) -> None:
        for worksheet in self.client.get_all_worksheets(spreadsheet_id=spreadsheet_id):
            self.import_worksheet(worksheet)

    def import_worksheet(self, worksheet: gspread.Worksheet) -> None:
        processor = WorksheetProcessorFactory.get_processor(
            worksheet_name=worksheet.title
        )

        entry = processor.process(worksheet)
        # repository = RepositoryFactory.get_repository(model_type=type(entry))
        # repository.add(entry)


if __name__ == "__main__":
    try:
        client = GoogleSheetsClient()
        import_service = GoogleSheetsImportService(
            google_sheets_client=client, db=database.get_db()
        )

        import_service.import_all_worksheets(spreadsheet_id=GOOGLE_SHEET_SPREADSHEET_ID)

    except Exception as error:
        print(error)

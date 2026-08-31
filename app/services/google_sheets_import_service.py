from config import GOOGLE_SHEET_SPREADSHEET_ID
import gspread
from app.api.integrations.google_sheets_client import GoogleSheetsClient


class GoogleSheetsImportService:
    def __init__(self, google_sheets_client: GoogleSheetsClient):
        self.google_sheets_client = google_sheets_client

    
        
        
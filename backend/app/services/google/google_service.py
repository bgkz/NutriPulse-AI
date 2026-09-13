import gspread
from app.config import GOOGLE_CREDENTIALS_PATH
from exceptions.google_service_exceptions import (
    GoogleSheetsError,
    SpreadsheetNotFoundError,
)


class GoogleService:
    def __init__(self):
        self.client = gspread.service_account(filename=GOOGLE_CREDENTIALS_PATH)

    def load(self, url: str) -> list[list[dict[str, int | float | str]]]:
        try:
            spreadsheet = self.client.open_by_url(url)

            return [
                worksheet.get_all_records() for worksheet in spreadsheet.worksheets()
            ]
        except gspread.SpreadsheetNotFound as error:
            raise SpreadsheetNotFoundError(
                f"Spreadsheet with URL: {url} not found"
            ) from error
        except gspread.exceptions.APIError as error:
            raise GoogleSheetsError("Google Sheets API error.") from error
        except gspread.exceptions.NoValidUrlKeyFound as error:
            raise GoogleSheetsError("No valid URL") from error

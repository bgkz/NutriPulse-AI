import gspread
from app.config import GOOGLE_CREDENTIALS_PATH
from exceptions.google_service_exceptions import (
    GoogleSheetsError,
    SpreadsheetNotFoundError,
    WorksheetNotFoundError,
)


class GoogleService:
    def __init__(self):
        self.client = gspread.service_account(filename=GOOGLE_CREDENTIALS_PATH)

    def verify_url(self, url: str) -> None:
        try:
            self.client.open_by_url(url)
        except gspread.SpreadsheetNotFound as error:
            raise SpreadsheetNotFoundError(
                f"Spreadsheet with URL: {url} not found"
            ) from error
        except gspread.exceptions.APIError as error:
            raise GoogleSheetsError("Google Sheets API error.") from error
        except gspread.exceptions.NoValidUrlKeyFound as error:
            raise GoogleSheetsError("No valid URL") from error

    def get_worksheet_names(self, url: str) -> list[str]:

        try:
            spreadsheet = self.client.open_by_url(url)
            return [worksheet.title for worksheet in spreadsheet.worksheets()]
        except gspread.SpreadsheetNotFound as error:
            raise SpreadsheetNotFoundError(
                f"Spreadsheet with URL: {url} not found"
            ) from error
        except gspread.exceptions.APIError as error:
            raise GoogleSheetsError("Google Sheets API error.") from error
        except gspread.exceptions.NoValidUrlKeyFound as error:
            raise GoogleSheetsError("No valid URL") from error

    def load(self, url: str, worksheet_name: str) -> list[dict[str, int | float | str]]:
        try:
            spreadsheet = self.client.open_by_url(url)

            worksheet = spreadsheet.worksheet(title=worksheet_name)

            return worksheet.get_all_records(numericise_ignore=["all"])
        except gspread.SpreadsheetNotFound as error:
            raise SpreadsheetNotFoundError(
                f"Spreadsheet with URL: {url} not found"
            ) from error
        except gspread.exceptions.APIError as error:
            raise GoogleSheetsError("Google Sheets API error.") from error
        except gspread.exceptions.NoValidUrlKeyFound as error:
            raise GoogleSheetsError("No valid URL") from error
        except gspread.WorksheetNotFound as error:
            raise WorksheetNotFoundError("Worksheet not found") from error

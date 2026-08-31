import gspread

from app import config
from exceptions.google_sheets_exceptions import (
    GoogleSheetsError,
    SpreadsheetNotFoundError,
    WorksheetNotFoundError,
)


class GoogleSheetsClient:
    def __init__(self) -> None:
        self.client = gspread.service_account(filename=config.GOOGLE_CREDENTIALS_PATH)

    def get_all_worksheets(self, spreadsheet_id: str) -> list[gspread.Worksheet]:
        try:
            spreadsheet = self.client.open_by_key(spreadsheet_id)
            return spreadsheet.worksheets()

        except gspread.exceptions.SpreadsheetNotFound as error:
            raise SpreadsheetNotFoundError(
                f"No Speadsheet found with id {spreadsheet_id}"
            ) from error
        except gspread.exceptions.APIError as error:
            raise GoogleSheetsError(
                "Failed to communicate with the Google Sheets API."
            ) from error

    def get_rows_by_worksheet_name(
        self,
        spreadsheet_id: str,
        worksheet_name: str,
    ) -> list[list[str]]:
        try:
            spreadsheet = self.client.open_by_key(spreadsheet_id)
            worksheet = spreadsheet.worksheet(worksheet_name)
            return worksheet.get_all_values()

        except gspread.exceptions.SpreadsheetNotFound as error:
            raise SpreadsheetNotFoundError(
                f"No Speadsheet found with id {spreadsheet_id}"
            ) from error
        except gspread.exceptions.WorksheetNotFound as error:
            raise WorksheetNotFoundError(
                f"No Worksheet found with name {worksheet_name}"
            ) from error
        except gspread.exceptions.APIError as error:
            raise GoogleSheetsError(
                "Failed to communicate with the Google Sheets API."
            ) from error

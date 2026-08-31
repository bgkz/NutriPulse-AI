import gspread

from app import config
from exceptions.google_sheets_exceptions import (
    GoogleSheetsAuthenticationError,
    GoogleSheetsError,
    SpreadsheetNotFoundError,
    WorksheetNotFoundError,
)


class GoogleSheetsClient:
    def __init__(self) -> None:
        try:
            self.client = gspread.service_account(
                filename=config.GOOGLE_CREDENTIALS_PATH
            )
        except (OSError, ValueError) as error:
            raise GoogleSheetsAuthenticationError(
                "Failed to initialize Google Sheets authentication."
            ) from error

    def get_all_worksheets(
        self,
        spreadsheet_id: str,
    ) -> list[gspread.Worksheet]:
        """
        Get all worksheets from a Google Sheets spreadsheet.

        Args:
            spreadsheet_id: The unique ID of the spreadsheet.

        Returns:
            A list of all worksheets contained in the spreadsheet.

        Raises:
            SpreadsheetNotFoundError:
                If no spreadsheet with the given ID could be found.
            GoogleSheetsError:
                If communication with the Google Sheets API fails.
        """
        try:
            spreadsheet = self.client.open_by_key(spreadsheet_id)
            return spreadsheet.worksheets()

        except gspread.exceptions.SpreadsheetNotFound as error:
            raise SpreadsheetNotFoundError(
                f"No spreadsheet found with id {spreadsheet_id}"
            ) from error

        except gspread.exceptions.APIError as error:
            raise GoogleSheetsError(
                "Failed to communicate with the Google Sheets API."
            ) from error

    def get_worksheet_by_name(
        self, spreadsheet_id: str, worksheet_name: str
    ) -> gspread.Worksheet:
        try:
            spreadsheet = self.client.open_by_key(spreadsheet_id)
            return spreadsheet.worksheet(worksheet_name)
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

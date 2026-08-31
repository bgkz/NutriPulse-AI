from types import SimpleNamespace

import pytest
from conftest import fake_get_all_values
from gspread.exceptions import APIError, SpreadsheetNotFound, WorksheetNotFound

from app.api.integrations.google_sheets_client import GoogleSheetsClient
from exceptions import google_sheets_exceptions


def test_get_rows_by_worksheet_name_success(
    fake_google_sheets_client: GoogleSheetsClient,
) -> None:

    result = fake_google_sheets_client.get_rows_by_worksheet_name(
        worksheet_name="test_worksheet", spreadsheet_id="test_id"
    )

    expected = fake_get_all_values()

    assert result == expected
    fake_google_sheets_client.client.open_by_key.assert_called_once_with("test_id")
    fake_google_sheets_client.client.spreadsheet.worksheet.assert_called_once_with(
        "test_worksheet"
    )


def test_get_rows_by_worksheet_name_throws_SpreadsheetNotFoundError(
    fake_google_sheets_client: GoogleSheetsClient,
) -> None:

    fake_google_sheets_client.client.open_by_key.side_effect = SpreadsheetNotFound

    with pytest.raises(
        google_sheets_exceptions.SpreadsheetNotFoundError,
        match="No Speadsheet found with id test_id",
    ):
        fake_google_sheets_client.get_rows_by_worksheet_name(
            worksheet_name="test_name", spreadsheet_id="test_id"
        )


def test_get_rows_by_worksheet_throws_WorksheetNotFoundError(
    fake_google_sheets_client: GoogleSheetsClient,
) -> None:

    fake_google_sheets_client.client.spreadsheet.worksheet.side_effect = (
        WorksheetNotFound
    )

    with pytest.raises(
        google_sheets_exceptions.WorksheetNotFoundError,
        match="No Worksheet found with name test_name",
    ):
        fake_google_sheets_client.get_rows_by_worksheet_name(
            worksheet_name="test_name", spreadsheet_id="test_id"
        )


def test_get_rows_by_worksheet_throws_GoogleSheetsError(
    fake_google_sheets_client: GoogleSheetsClient,
) -> None:

    response = SimpleNamespace(text="This is a fake Exception-Text")
    fake_google_sheets_client.client.worksheet.get_all_values.side_effect = APIError(
        response
    )

    with pytest.raises(
        google_sheets_exceptions.GoogleSheetsError,
        match="Failed to communicate with the Google Sheets API.",
    ):
        fake_google_sheets_client.get_rows_by_worksheet_name(
            worksheet_name="test_name", spreadsheet_id="test_id"
        )

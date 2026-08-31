from pathlib import Path
from unittest.mock import MagicMock

import gspread
import pytest
from pytest import MonkeyPatch

from app.api.integrations.google_sheets_client import GoogleSheetsClient


def fake_get_all_values() -> list[list[str]]:
    return [
        ["Datum", "Training", "Cardio", "Kalorien", "Protein", "Fett", "KH"],
        ["25.4", "GK Push", "8000", "2600 schätzungswese", "140", "42", "104"],
    ]


class FakeGoogleClient:
    def __init__(self, filename: Path | str):
        self.spreadsheet = MagicMock()
        self.worksheet = MagicMock()
        self.open_by_key = MagicMock()

        self.worksheet.get_all_values.return_value = fake_get_all_values()
        self.spreadsheet.worksheet.return_value = self.worksheet
        self.open_by_key.return_value = self.spreadsheet


@pytest.fixture
def fake_google_sheets_client(monkeypatch: MonkeyPatch) -> GoogleSheetsClient:
    monkeypatch.setattr(gspread, "service_account", FakeGoogleClient)
    return GoogleSheetsClient()

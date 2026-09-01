import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


GOOGLE_SHEETS_API_KEY = os.getenv("GOOGLE_SHEETS_API_KEY")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
GOOGLE_SHEET_SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_SPREADSHEET_ID")
TRAINING_WORKSHEET_NAME = os.getenv("TRAINING_WORKSHEET_NAME")
NUTRITION_WORKSHEET_NAME = os.getenv("NUTRITION_WORKSHEET_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
BACKEND_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BACKEND_DIR / "storage"

STORAGE_DIR.mkdir(exist_ok=True)


GOOGLE_SHEETS_API_KEY = os.getenv("GOOGLE_SHEETS_API_KEY")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
GOOGLE_SHEET_SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_SPREADSHEET_ID")
TRAINING_WORKSHEET_NAME = os.getenv("TRAINING_WORKSHEET_NAME")
NUTRITION_WORKSHEET_NAME = os.getenv("NUTRITION_WORKSHEET_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODE = "mock"

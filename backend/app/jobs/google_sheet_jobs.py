from app.services.google.google_service import GoogleService


def load_google_sheet_job(url: str):
    service = GoogleService()
    return service.load(url)

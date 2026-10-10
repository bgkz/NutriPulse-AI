from app.services.google.google_service import GoogleService


def load_google_sheets_data(url: str):
    service = GoogleService()
    return service.load(url)


def verify_url(url: str):
    service = GoogleService()

    service.verify_url(url)

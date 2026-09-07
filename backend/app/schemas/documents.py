from pydantic import BaseModel


class UrlImportRequest(BaseModel):
    url: str

from app.core.security import decode_access_token
from app.database import get_db
from app.schemas.documents import UrlImportRequest
from exceptions.security_exceptions import InvalidAccessTokenError
from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/documents")


@router.post("/", status_code=status.HTTP_200_OK)
async def import_url(
    data: UrlImportRequest,
    authorization: str = Header(),
    db: Session = Depends(get_db),  # noqa: B008
):
    try:
        token = authorization.removeprefix("Bearer ")
        payload = decode_access_token(token)
        user_id = payload["sub"]
        print(user_id)
        print(data.url)

        return {"message": "ok"}

    except InvalidAccessTokenError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))

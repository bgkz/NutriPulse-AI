from uuid import UUID

from app.core.security import decode_access_token
from app.database import get_db
from app.models.conversation_entry import ConversationEntry
from app.repositories.conversation_repository import ConversationRepository
from app.services.conversation_service import ConversationService
from exceptions.security_exceptions import InvalidAccessTokenError
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/conversations")


@router.get("/", status_code=status.HTTP_200_OK)
def get_conversations(
    authorization: str = Header(),
    db: Session = Depends(get_db),  # noqa: B008
):
    try:
        token = authorization.removeprefix("Bearer ")
        payload = decode_access_token(token)
        user_id = UUID(payload["sub"])
        print(user_id)
        conversation_service = ConversationService(ConversationRepository(db=db))

        return conversation_service.get_conversations_by_user(user_id)

    except InvalidAccessTokenError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))

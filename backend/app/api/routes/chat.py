from app.core.security import decode_access_token
from app.database import get_db
from app.models.conversation_entry import ConversationEntry
from app.repositories.chat.chat_repository import ChatRepository
from app.schemas.chat import ChatRequest
from app.services.chat.chat_service import ChatService
from exceptions.security_exceptions import InvalidAccessTokenError
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat")


@router.post("/")
async def send_message(
    chat_request: ChatRequest,
    authorization: str = Header(),
    db: Session = Depends(get_db),  # noqa: B008
):
    try:
        token = authorization.removeprefix("Bearer ")
        payload = decode_access_token(token=token)
        user_id = payload["sub"]
        chat_service = ChatService(ChatRepository(db=db))

    except InvalidAccessTokenError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))

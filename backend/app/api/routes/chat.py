from uuid import UUID

from app.core.security import decode_access_token
from app.database import get_db
from app.repositories.chat.chat_repository import ChatRepository
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.chat import SendMessageRequest
from app.services.chat.chat_service import ChatService
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from exceptions.security_exceptions import InvalidAccessTokenError
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat")


@router.post("/")
async def send_message(
    send_message_request: SendMessageRequest,
    authorization: str = Header(),
    db: Session = Depends(get_db),  # noqa: B008
):
    try:
        token = authorization.removeprefix("Bearer ")
        payload = decode_access_token(token=token)
        user_id = UUID(payload["sub"])

        conversation_service = ConversationService(ConversationRepository(db=db))
        message_service = MessageService(MessageRepository(db=db))

        chat_service = ChatService(conversation_service, message_service)

        if not send_message_request.conversation_id:
            conversation_created = chat_service.create_conversation(user_id)
            send_message_request.conversation_id = conversation_created.id
            
        message_created = chat_service.create_message(send_message_request)


    except InvalidAccessTokenError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))

    except Exception as error:
        print(error)

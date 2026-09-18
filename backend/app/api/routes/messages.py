from uuid import UUID

from app.database import get_db
from app.repositories.message_repository import MessageRepository
from app.services.message_service import MessageService
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/messages")


@router.get("/{conversation_id}")
def get_messages(
    conversation_id: str,
    db: Session = Depends(get_db),  # noqa: B008
):
    message_service = MessageService(MessageRepository(db=db))

    messages = message_service.get_messages_by_conversation_id(UUID(conversation_id))
    print(messages)
    return messages

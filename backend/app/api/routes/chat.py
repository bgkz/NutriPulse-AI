from uuid import UUID

from app.core.security import decode_access_token
from app.database import get_db
from app.jobs.jobs import generate_llm_response
from app.queue import queue, redis_connection
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.chat import SendMessageRequest, SendMessageResponse
from app.services.chat.chat_service import ChatService
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from exceptions.repository_exceptions import RepositoryError
from exceptions.security_exceptions import InvalidAccessTokenError
from fastapi import APIRouter, Depends, Header, HTTPException, status
from rq.exceptions import NoSuchJobError
from rq.job import Job
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat")


@router.post(
    "/", response_model=SendMessageResponse, status_code=status.HTTP_202_ACCEPTED
)
async def send_message(
    send_message_request: SendMessageRequest,
    authorization: str = Header(),
    db: Session = Depends(get_db),  # noqa: B008
) -> SendMessageResponse:
    try:
        token = authorization.removeprefix("Bearer ")
        payload = decode_access_token(token=token)
        user_id = UUID(payload["sub"])

        conversation_service = ConversationService(ConversationRepository(db=db))
        message_service = MessageService(MessageRepository(db=db))

        chat_service = ChatService(conversation_service, message_service)

        active_conversation = chat_service.get_conversation(
            send_message_request.conversation_id
        )

        if active_conversation and active_conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
            )

        if not active_conversation:
            active_conversation = chat_service.create_conversation(user_id=user_id)

        send_message_request.conversation_id = active_conversation.id
        message_created = chat_service.create_message(send_message_request)

        job = queue.enqueue(generate_llm_response, active_conversation.id)

        return SendMessageResponse.model_validate(
            {
                "conversation": active_conversation,
                "message": message_created,
                "job": job.id,
            }
        )

    except InvalidAccessTokenError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))

    except RepositoryError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )


@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_connection)
        if job.is_finished:
            return {"status": job.get_status(), "result": job.result}
        if job.is_failed:
            return {"status": "failed", "error": job.exc_info}
        if not job.is_finished:
            return {"status": job.get_status(), "result": None}

    except NoSuchJobError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

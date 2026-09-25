from typing import Any
from uuid import UUID

from app.jobs.document_jobs import complete_document_import, save_document_in_db
from app.jobs.fitness_service_jobs import save_fitness_entries
from app.jobs.google_sheet_jobs import load_google_sheets_data
from app.jobs.llm_service_jobs import generate_response, parse_sheets_data
from app.jobs.message_jobs import add_message_to_db, get_messages_by_conversation_id
from app.models.message_entry import RoleType
from app.queue import queue
from rq.job import Job


def generate_llm_response(conversation_id: UUID):
    messages = get_messages_by_conversation_id(conversation_id=conversation_id)
    llm_messages = [
        {"role": message.role.value, "content": message.content} for message in messages
    ]
    response_text = generate_response(input=llm_messages)
    message_added = add_message_to_db(
        conversation_id=conversation_id, message=response_text, role=RoleType.ASSISTANT
    )
    return message_added


def run_import(url: str, user_id: Any) -> dict[str, Any]:
    """Run the import as one RQ job; any exception fails the entire job."""
    sheets_data = load_google_sheets_data(url)
    document = save_document_in_db(user_id, url)
    parsed_data = parse_sheets_data(sheets_data)
    save_fitness_entries(parsed_data, document)
    return complete_document_import(document, parsed_data)


def process_import(url: str, user_id: Any) -> Job:
    # The timeout now covers all five steps, previously separate RQ jobs.
    return queue.enqueue(run_import, url, user_id, job_timeout=900)

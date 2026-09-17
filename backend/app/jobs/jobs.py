from typing import Any

from app.jobs.document_jobs import complete_document_import, save_document_in_db
from app.jobs.fitness_service_jobs import save_fitness_entries
from app.jobs.google_sheet_jobs import load_google_sheets_data
from app.jobs.llm_service_jobs import parse_sheets_data
from app.queue import queue
from rq.job import Job


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

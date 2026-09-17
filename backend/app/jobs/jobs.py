from typing import Any

from app.jobs.document_jobs import (
    save_document_in_db,
    update_document_processing_status_to_success,
)
from app.jobs.fitness_service_jobs import save_parsed_fitness_entries_in_db
from app.jobs.google_sheet_jobs import load_google_sheets_data
from app.jobs.llm_service_jobs import parse_data_with_llm
from app.queue import queue


def process_import(url: str, user_id: Any):
    try:
        job_load_google_sheets_data = queue.enqueue(
            load_google_sheets_data,
            url,
        )

        job_save_document_in_db = queue.enqueue(save_document_in_db, user_id, url)

        job_parse_sheets_data_with_llm = queue.enqueue(
            parse_data_with_llm,
            job_load_google_sheets_data.id,
            depends_on=job_load_google_sheets_data,
        )

        job_save_fitness_entries = queue.enqueue(
            save_parsed_fitness_entries_in_db,
            job_parse_sheets_data_with_llm.id,
            job_save_document_in_db.id,
            depends_on=[
                job_parse_sheets_data_with_llm,
                job_save_document_in_db,
            ],
        )

        return queue.enqueue(
            update_document_processing_status_to_success,
            job_save_document_in_db.id,
            job_parse_sheets_data_with_llm.id,
            depends_on=job_save_fitness_entries,
        )
    except Exception as error:
        print(error)
        raise

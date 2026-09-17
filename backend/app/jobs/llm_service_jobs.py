import asyncio

from app.config import LLM_MODE, STORAGE_DIR
from app.queue import redis_connection
from app.schemas.fitness import FitnessEntries
from app.services.llm.llm_service import LLMService
from rq.job import Job


def parse_data_with_llm(previous_job_id: str):
    previous_job = Job.fetch(
        previous_job_id,
        connection=redis_connection,
    )

    data = previous_job.result
    return parse_sheets_data(data)


def parse_sheets_data(data):

    if LLM_MODE == "mock":
        file_path = STORAGE_DIR / "llm_parsed_entries.json"
        parsed_data = FitnessEntries.model_validate_json(
            file_path.read_text(encoding="utf-8")
        )
    elif LLM_MODE == "live":
        llm_service = LLMService()
        parsed_data = asyncio.run(llm_service.get_llm_response(data))

        if parsed_data is None:
            raise ValueError("LLM returned no structured fitness data")
    else:
        raise ValueError(f"Unknown LLM_MODE: {LLM_MODE}")

    return parsed_data.model_dump(mode="json")


def get_llm_response_job(sheets_data):
    return parse_data_with_llm(sheets_data)

import asyncio

from app.services.llm.llm_service import LLMService


def parse_data_with_llm(data):
    llm_service = LLMService()

    parsed_data = asyncio.run(llm_service.get_llm_response(data))

    if parsed_data is None:
        raise ValueError("LLM returned no structured fitness data")

    return parsed_data.model_dump(mode="json")


def get_llm_response_job(sheets_data):
    return parse_data_with_llm(sheets_data)

import json

from app.config import OPENAI_API_KEY
from app.schemas.fitness import FitnessEntries
from openai import AsyncOpenAI


class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def get_llm_response(self, data):
        try:
            response = await self.client.responses.parse(
                model="gpt-5.6-terra",
                input=json.dumps(data, ensure_ascii=False),
                instructions="""
                Normalize the provided fitness data.

                Identify nutrition and workout data.

                Pay close attention to dates:
                - Preserve the correct date for each data entry.
                - Associate nutrition and workout data with the exact date they belong to.
                - Do not move, merge, or assign data to a different date.
                - If a date cannot be determined reliably, use null.
                - Preserve the original date information in notes if it is ambiguous.

                Do not invent values.
                Use null when a field cannot be determined.
                Convert units into the schema's units.
                Preserve uncertain information in notes.

                If any error happens while converting, return exactly:
                "Error returned while converting data"
                """,
                text_format=FitnessEntries,
            )

            return response.output_parsed
        except Exception as e:
            print(str(e))

import json
from typing import Any

from app.config import OPENAI_API_KEY
from app.schemas.fitness import FitnessEntries
from app.services.llm import settings
from openai import AsyncOpenAI


class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate_response(self, input: Any, instructions: str | None) -> str:
        try:
            response = await self.client.responses.create(
                model=settings.GPT_MODEL, input=input, instructions=instructions
            )

            return response.output_text
        except Exception as error:
            print("An exception occurred in LLMService: ", error)
            raise

    async def get_llm_response(self, data):
        try:
            response = await self.client.responses.parse(
                model=settings.GPT_MODEL,
                input=json.dumps(data, ensure_ascii=False),
                instructions="""
                Normalize the provided fitness data.

                Identify nutrition and workout data.

                WORKOUT DATA RULES:

                - Create ONE WorkoutData entry PER EXERCISE.
                - Never combine multiple exercises into one WorkoutData entry.
                - Never use generic exercise names such as "Workout log".
                - The exercise field must contain the actual exercise name.

                - Repetition notation such as:
                    80kg 7/6/4
                means:
                    weight_kg = 80
                    reps_in_set_one = 7
                    reps_in_set_two = 6
                    reps_in_set_three = 4

                - Example:
                    "Bench press 80kg 7/6/4"
                must become:
                    exercise = "Bench Press"
                    weight_kg = 80
                    reps_in_set_one = 7
                    reps_in_set_two = 6
                    reps_in_set_three = 4

                - If only two sets are provided, for example:
                    "Deadlift 110kg 5/3"
                use:
                    reps_in_set_one = 5
                    reps_in_set_two = 3
                    reps_in_set_three = null

                - If multiple exercises occur on the same date, create separate
                WorkoutData entries with the same date.

                - If the weight changes between sets, do not pretend that one weight
                applies to every set. Preserve additional weight/set information
                in notes when it cannot be represented accurately by the schema.

                DATE RULES:

                - Preserve the correct date for each data entry.
                - Associate nutrition and workout data with the exact date they belong to.
                - Do not move, merge, or assign data to a different date.
                - If a date cannot be determined reliably, use null.
                - Preserve the original date information in notes if it is ambiguous.

                GENERAL RULES:

                - Do not invent values.
                - Use null when a field cannot be determined.
                - Convert units into the schema's units.
                - Preserve uncertain information in notes.
                """,
                text_format=FitnessEntries,
                temperature=settings.GPT_TEMPERATURE,
            )

            return response.output_parsed
        except Exception as e:
            print(str(e))
            raise

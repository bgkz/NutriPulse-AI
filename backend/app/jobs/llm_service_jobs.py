import asyncio
from collections.abc import Callable
from typing import Any
from uuid import UUID

from app.services.llm.llm_service import LLMService


def generate_response(
    input: Any,
    instructions: str | None,
    user_id: UUID | None = None,
    on_delta: Callable[[str], None] | None = None,
) -> str:
    llm_service = LLMService()

    return asyncio.run(
        llm_service.generate_response(
            input=input,
            instructions=instructions,
            user_id=user_id,
            on_delta=on_delta,
        )
    )

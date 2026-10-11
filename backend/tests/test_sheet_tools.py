import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from app.services.llm import llm_service, sheet_tools


class FakeResponseStream:
    """Model the SDK's async context manager and event iterator without networking."""

    def __init__(self, response, events=()):
        self.events = events
        self.get_final_response = AsyncMock(return_value=response)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return False

    async def __aiter__(self):
        for event in self.events:
            yield event


def test_tool_result_is_sent_back_before_final_answer(monkeypatch):
    call = SimpleNamespace(
        type="function_call", name="read_sheet",
        arguments='{"document_id": "doc-1", "worksheet_name": "Workout"}', call_id="call-1",
    )
    reasoning_data = {"type": "reasoning", "id": "reasoning-1", "summary": []}
    reasoning = SimpleNamespace(
        type="reasoning",
        model_dump=Mock(return_value={**reasoning_data, "status": "completed"}),
    )
    create = Mock(side_effect=[
        FakeResponseStream(SimpleNamespace(output=[reasoning, call], output_text="")),
        FakeResponseStream(SimpleNamespace(output=[], output_text="Dein Gewicht ist gesunken.")),
    ])
    monkeypatch.setattr(llm_service, "AsyncOpenAI", lambda **kwargs: SimpleNamespace(
        responses=SimpleNamespace(stream=create)
    ))
    monkeypatch.setattr(llm_service, "get_user_documents", Mock(return_value={"doc-1": "url"}))
    execute = Mock(return_value={"data": [{"weight": 80}]})
    monkeypatch.setattr(llm_service, "execute_sheet_tool", execute)

    result = asyncio.run(llm_service.LLMService().generate_response(
        [{"role": "user", "content": "Wie läuft mein Training?"}], None, uuid4()
    ))

    assert result == "Dein Gewicht ist gesunken."
    execute.assert_called_once_with("read_sheet", call.arguments, {"doc-1": "url"})
    history = create.call_args_list[1].kwargs["input"]
    reasoning.model_dump.assert_called_once_with(mode="json", exclude_none=True)
    assert history[1] == reasoning_data
    assert history[2] == {
        "type": "function_call",
        "call_id": "call-1",
        "name": "read_sheet",
        "arguments": call.arguments,
    }
    assert history[-1]["call_id"] == "call-1"
    assert json.loads(history[-1]["output"]) == {"data": [{"weight": 80}]}


def test_title_generation_does_not_load_documents(monkeypatch):
    create = Mock(return_value=FakeResponseStream(SimpleNamespace(output=[], output_text="Titel")))
    monkeypatch.setattr(llm_service, "AsyncOpenAI", lambda **kwargs: SimpleNamespace(
        responses=SimpleNamespace(stream=create)
    ))
    documents = Mock()
    monkeypatch.setattr(llm_service, "get_user_documents", documents)

    assert asyncio.run(llm_service.LLMService().generate_response("Chat", "Titel")) == "Titel"
    documents.assert_not_called()
    assert create.call_args.kwargs["tools"] == []


def test_foreign_document_is_rejected_before_google_access(monkeypatch):
    google = Mock()
    monkeypatch.setattr(sheet_tools, "GoogleService", google)
    result = sheet_tools.execute_sheet_tool(
        "read_sheet", '{"document_id": "foreign"}', {"own": "url"}
    )
    assert "error" in result
    google.assert_not_called()


def test_allowed_document_is_loaded(monkeypatch):
    google = Mock()
    google.return_value.load.return_value = [[{"weight": 80}]]
    monkeypatch.setattr(sheet_tools, "GoogleService", google)
    result = sheet_tools.execute_sheet_tool("read_sheet", '{"document_id": "own", "worksheet_name": "Workout"}', {"own": "url"})
    google.return_value.load.assert_called_once_with("url", "Workout")
    assert result["data"] == [[{"weight": 80}]]


def test_sheet_failure_is_returned_to_model(monkeypatch):
    google = Mock()
    google.return_value.load.side_effect = RuntimeError("private details")
    monkeypatch.setattr(sheet_tools, "GoogleService", google)
    result = sheet_tools.execute_sheet_tool("read_sheet", '{"document_id": "own", "worksheet_name": "Workout"}', {"own": "url"})
    google.return_value.load.assert_called_once_with("url", "Workout")
    assert "error" in result
    assert "private details" not in result["error"]


def test_stream_forwards_only_text_deltas(monkeypatch):
    events = [
        SimpleNamespace(type="response.created"),
        SimpleNamespace(type="response.output_text.delta", delta="Hallo "),
        SimpleNamespace(type="response.function_call_arguments.delta", delta="{}"),
        SimpleNamespace(type="response.output_text.delta", delta="Welt"),
    ]
    stream = FakeResponseStream(
        SimpleNamespace(output=[], output_text="Hallo Welt"), events
    )
    monkeypatch.setattr(llm_service, "AsyncOpenAI", lambda **kwargs: SimpleNamespace(
        responses=SimpleNamespace(stream=Mock(return_value=stream))
    ))
    callback = Mock()
    result = asyncio.run(llm_service.LLMService().generate_response(
        "Hallo", None, on_delta=callback
    ))
    assert result == "Hallo Welt"
    assert [call.args[0] for call in callback.call_args_list] == ["Hallo ", "Welt"]
    stream.get_final_response.assert_awaited_once()


def test_missing_worksheet_is_rejected_before_google_access(monkeypatch):
    google = Mock()
    monkeypatch.setattr(sheet_tools, "GoogleService", google)
    result = sheet_tools.execute_sheet_tool(
        "read_sheet", '{"document_id": "own"}', {"own": "url"}
    )
    assert "error" in result
    google.assert_not_called()


def test_worksheets_are_listed_for_allowed_document(monkeypatch):
    google = Mock()
    google.return_value.get_worksheet_names.return_value = ["Workout", "Nutrition"]
    monkeypatch.setattr(sheet_tools, "GoogleService", google)
    result = sheet_tools.execute_sheet_tool(
        "list_worksheets", '{"document_id": "own"}', {"own": "url"}
    )
    google.return_value.get_worksheet_names.assert_called_once_with("url")
    assert result["worksheets"] == ["Workout", "Nutrition"]

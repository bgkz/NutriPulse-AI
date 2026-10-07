import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from app.services.llm import llm_service, sheet_tools


def test_tool_result_is_sent_back_before_final_answer(monkeypatch):
    call = SimpleNamespace(
        type="function_call", name="read_sheet",
        arguments='{"document_id": "doc-1"}', call_id="call-1",
    )
    reasoning = SimpleNamespace(type="reasoning")
    create = AsyncMock(side_effect=[
        SimpleNamespace(output=[reasoning, call], output_text=""),
        SimpleNamespace(output=[], output_text="Dein Gewicht ist gesunken."),
    ])
    monkeypatch.setattr(llm_service, "AsyncOpenAI", lambda **kwargs: SimpleNamespace(
        responses=SimpleNamespace(create=create)
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
    assert reasoning in history
    assert history[-1]["call_id"] == "call-1"
    assert json.loads(history[-1]["output"]) == {"data": [{"weight": 80}]}


def test_title_generation_does_not_load_documents(monkeypatch):
    create = AsyncMock(return_value=SimpleNamespace(output=[], output_text="Titel"))
    monkeypatch.setattr(llm_service, "AsyncOpenAI", lambda **kwargs: SimpleNamespace(
        responses=SimpleNamespace(create=create)
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
    result = sheet_tools.execute_sheet_tool("read_sheet", '{"document_id": "own"}', {"own": "url"})
    google.return_value.load.assert_called_once_with("url")
    assert result["data"] == [[{"weight": 80}]]


def test_sheet_failure_is_returned_to_model(monkeypatch):
    google = Mock()
    google.return_value.load.side_effect = RuntimeError("private details")
    monkeypatch.setattr(sheet_tools, "GoogleService", google)
    result = sheet_tools.execute_sheet_tool("read_sheet", '{"document_id": "own"}', {"own": "url"})
    assert "error" in result
    assert "private details" not in result["error"]

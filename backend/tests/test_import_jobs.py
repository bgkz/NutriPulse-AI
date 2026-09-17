import os
from unittest.mock import Mock
from uuid import uuid4

import pytest
from redis import Redis
from rq import Queue, SimpleWorker
from rq.timeouts import TimerDeathPenalty

from app.jobs import jobs
from exceptions.google_service_exceptions import SpreadsheetNotFoundError


STEPS = (
    "load_google_sheets_data",
    "save_document_in_db",
    "parse_sheets_data",
    "save_fitness_entries",
    "complete_document_import",
)


@pytest.fixture
def steps(monkeypatch):
    mocks = {}
    for name in STEPS:
        mocks[name] = Mock()
        monkeypatch.setattr(jobs, name, mocks[name])
    return mocks


def test_success_passes_data_between_steps(steps):
    result = jobs.run_import("sheet-url", "user-id")
    steps[STEPS[0]].assert_called_once_with("sheet-url")
    steps[STEPS[1]].assert_called_once_with("user-id", "sheet-url")
    steps[STEPS[2]].assert_called_once_with(steps[STEPS[0]].return_value)
    steps[STEPS[3]].assert_called_once_with(
        steps[STEPS[2]].return_value, steps[STEPS[1]].return_value
    )
    steps[STEPS[4]].assert_called_once_with(
        steps[STEPS[1]].return_value, steps[STEPS[2]].return_value
    )
    assert result is steps[STEPS[4]].return_value


@pytest.mark.parametrize("failed_step", range(len(STEPS)))
def test_failure_propagates_and_stops_remaining_steps(steps, failed_step):
    error = RuntimeError("Import step failed")
    steps[STEPS[failed_step]].side_effect = error
    with pytest.raises(RuntimeError) as raised:
        jobs.run_import("sheet-url", "user-id")
    assert raised.value is error
    for name in STEPS[failed_step + 1:]:
        steps[name].assert_not_called()


@pytest.mark.skipif(
    not os.getenv("TEST_REDIS_URL"), reason="Set TEST_REDIS_URL for the RQ integration test"
)
@pytest.mark.parametrize("fail", [False, True])
def test_worker_persists_overall_status(monkeypatch, steps, fail):
    connection = Redis.from_url(os.environ["TEST_REDIS_URL"])
    queue = Queue(f"test-import-{uuid4().hex}", connection=connection)
    monkeypatch.setattr(jobs, "queue", queue)
    steps[STEPS[-1]].return_value = {"nutrition": [], "workouts": []}
    if fail:
        steps[STEPS[0]].side_effect = SpreadsheetNotFoundError("Sheet not found")

    class TestWorker(SimpleWorker):
        death_penalty_class = TimerDeathPenalty

    job = jobs.process_import("invalid-sheet-url", "user-id")
    worker = TestWorker([queue], connection=connection)
    try:
        worker.work(burst=True, with_scheduler=False, logging_level="CRITICAL")
        job.refresh()
        assert job.get_status() == ("failed" if fail else "finished")
        if fail:
            assert job.id in queue.failed_job_registry.get_job_ids()
            assert "SpreadsheetNotFoundError" in job.exc_info
            steps["save_document_in_db"].assert_not_called()
        else:
            assert job.return_value() == {"nutrition": [], "workouts": []}
    finally:
        job.delete()
        queue.delete()
        connection.delete(worker.key)

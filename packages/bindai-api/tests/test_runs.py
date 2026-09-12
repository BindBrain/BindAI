from __future__ import annotations

from bindai_api.app import (
    app,
    configure_automation,
)
from bindai_automation import AutomationDefinition
from bindai_core.executable import Executable, ExecutionResult
from fastapi.testclient import TestClient

TEST_API_KEY = "test-api-key"
AUTH_HEADERS = {
    "Authorization": f"Bearer {TEST_API_KEY}",
}


class SampleExecutable(Executable):
    def execute(self, context) -> ExecutionResult:
        return ExecutionResult(
            success=True,
            output="done",
        )


class FailingExecutable(Executable):
    def execute(self, context) -> ExecutionResult:
        return ExecutionResult(
            success=False,
            error="failed",
        )


def make_automation(
    executable: Executable | None = None,
) -> AutomationDefinition:
    return AutomationDefinition(
        name="test-automation",
        target=executable or SampleExecutable(),
    )


def test_run_not_found(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    client = TestClient(app)

    response = client.get(
        "/api/v1/runs/missing",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Run 'missing' was not found.",
    }


def test_create_run(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    automation = make_automation()
    configure_automation(automation)

    client = TestClient(app)

    response = client.post(
        "/api/v1/runs",
        json={
            "automation_id": automation.id,
            "input": {
                "message": "hello",
            },
        },
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 202

    body = response.json()

    assert body["id"]
    assert body["definition_id"] == automation.id
    assert body["definition_version"] == automation.version
    assert body["input"] == {
        "message": "hello",
    }
    assert body["status"] in {
        "pending",
        "running",
        "completed",
    }


def test_get_run_after_execution(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    automation = make_automation()
    configure_automation(automation)

    client = TestClient(app)

    create_response = client.post(
        "/api/v1/runs",
        json={
            "automation_id": automation.id,
            "input": "hello",
        },
        headers=AUTH_HEADERS,
    )

    assert create_response.status_code == 202

    run_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/runs/{run_id}",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == run_id
    assert body["definition_id"] == automation.id
    assert body["status"] == "completed"
    assert body["input"] == "hello"
    assert body["output"] == "done"
    assert body["error"] is None
    assert body["created_at"] is not None
    assert body["started_at"] is not None
    assert body["completed_at"] is not None


def test_create_run_automation_not_found(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/runs",
        json={
            "automation_id": "missing",
        },
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Automation 'missing' was not found.",
    }


def test_create_run_handles_failed_automation(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    automation = make_automation(FailingExecutable())
    configure_automation(automation)

    client = TestClient(app)

    response = client.post(
        "/api/v1/runs",
        json={
            "automation_id": automation.id,
        },
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 202

    run_id = response.json()["id"]

    response = client.get(
        f"/api/v1/runs/{run_id}",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "failed"
    assert body["output"] is None
    assert body["error"] == "failed"


def test_runs_require_api_key(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    client = TestClient(app)

    response = client.get("/api/v1/runs/missing")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid or missing API key.",
    }

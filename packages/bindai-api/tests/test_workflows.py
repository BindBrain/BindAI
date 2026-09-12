from __future__ import annotations

from bindai_api.app import app
from bindai_core.context import ExecutionContext
from bindai_workflow import Workflow, WorkflowRegistry
from fastapi.testclient import TestClient

TEST_API_KEY = "test-api-key"

AUTH_HEADERS = {
    "Authorization": f"Bearer {TEST_API_KEY}",
}


def test_workflow_not_found(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    WorkflowRegistry.clear()

    client = TestClient(app)

    response = client.post(
        "/api/v1/workflows/missing/run",
        json={"variables": {"message": "hello"}},
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Workflow 'missing' was not found.",
    }


def test_list_workflows(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    WorkflowRegistry.clear()

    workflow = Workflow(name="test-workflow")
    WorkflowRegistry.register(workflow)

    client = TestClient(app)

    response = client.get(
        "/api/v1/workflows",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": workflow.id,
            "name": "test-workflow",
        }
    ]

    WorkflowRegistry.clear()


def test_workflow_run(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    WorkflowRegistry.clear()

    workflow = Workflow(name="test-workflow")
    WorkflowRegistry.register(workflow)

    captured: dict[str, object] = {}

    def fake_run(context: ExecutionContext):
        captured.update(context.variables)

        return {
            "status": "completed",
            "message": "hello",
        }

    monkeypatch.setattr(
        workflow,
        "run",
        fake_run,
    )

    client = TestClient(app)

    response = client.post(
        f"/api/v1/workflows/{workflow.id}/run",
        json={
            "variables": {
                "message": "hello",
                "user": "test-user",
            }
        },
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == {
        "workflow": workflow.id,
        "result": {
            "status": "completed",
            "message": "hello",
        },
    }

    assert captured == {
        "message": "hello",
        "user": "test-user",
    }

    WorkflowRegistry.clear()

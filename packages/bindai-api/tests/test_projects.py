from __future__ import annotations

from bindai_api.app import app, configure_project
from bindai_project import Project, ProjectConfiguration
from fastapi.testclient import TestClient

TEST_API_KEY = "test-api-key"

AUTH_HEADERS = {
    "Authorization": f"Bearer {TEST_API_KEY}",
}


def create_project(name: str) -> Project:
    return Project(
        ProjectConfiguration(
            name=name,
        )
    )


def test_project_not_found(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    client = TestClient(app)

    response = client.get(
        "/api/v1/projects/missing",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Project 'missing' was not found.",
    }


def test_list_projects(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    project = create_project("test-project")
    configure_project(project)

    client = TestClient(app)

    response = client.get(
        "/api/v1/projects",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "test-project",
        }
    ]


def test_get_project(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    project = create_project("test-project")
    configure_project(project)

    client = TestClient(app)

    response = client.get(
        "/api/v1/projects/test-project",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == {
        "name": "test-project",
    }


def test_projects_require_api_key(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    client = TestClient(app)

    response = client.get("/api/v1/projects/missing")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid or missing API key.",
    }

from __future__ import annotations

from bindai.application import Application
from bindai.application.configuration import ApplicationConfiguration
from bindai_agent import Agent
from bindai_api.app import app, configure_application
from fastapi.testclient import TestClient

TEST_API_KEY = "test-api-key"
AUTH_HEADERS = {
    "Authorization": f"Bearer {TEST_API_KEY}",
}


def create_application() -> Application:
    application = Application(
        configuration=ApplicationConfiguration(
            name="test-application",
        )
    )

    agent = Agent.builder().name("assistant").build()
    application.add_agent(agent)

    return application


def test_health_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "bindai-api",
    }


def test_agent_not_found(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    configure_application(create_application())

    client = TestClient(app)

    response = client.post(
        "/api/v1/agents/missing/run",
        json={"message": "hello"},
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Agent 'missing' was not found.",
    }


def test_agent_stream(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    application = create_application()
    agent = application.agents.all()[0]

    def fake_stream_chat(message: str):
        assert message == "hello"
        return iter(["Hello", " ", "world"])

    monkeypatch.setattr(
        agent,
        "stream_chat",
        fake_stream_chat,
    )

    configure_application(application)

    client = TestClient(app)

    response = client.post(
        "/api/v1/agents/assistant/stream",
        json={"message": "hello"},
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.text == "Hello world"
    assert response.headers["content-type"].startswith("text/plain")


def test_agent_requires_api_key(monkeypatch) -> None:
    monkeypatch.setenv(
        "BINDAI_API_KEY",
        TEST_API_KEY,
    )

    configure_application(create_application())

    client = TestClient(app)

    response = client.post(
        "/api/v1/agents/assistant/run",
        json={"message": "hello"},
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid or missing API key.",
    }

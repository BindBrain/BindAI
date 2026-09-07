from unittest.mock import MagicMock

import pytest

from bindai_connections import JiraConnection


def test_jira_connection_lifecycle():
    connection = JiraConnection(
        "test-token",
        base_url="https://example.atlassian.net",
    )

    assert connection.name == "jira"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_jira_connection_rejects_empty_token():
    with pytest.raises(ValueError, match="Jira token cannot be empty"):
        JiraConnection(
            "",
            base_url="https://example.atlassian.net",
        )


def test_jira_connection_rejects_empty_base_url():
    with pytest.raises(ValueError, match="Jira base URL cannot be empty"):
        JiraConnection(
            "test-token",
            base_url="",
        )


def test_jira_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Jira timeout must be greater than zero",
    ):
        JiraConnection(
            "test-token",
            base_url="https://example.atlassian.net",
            timeout=0,
        )


def test_jira_connection_rejects_inactive_send():
    connection = JiraConnection(
        "test-token",
        base_url="https://example.atlassian.net",
    )

    with pytest.raises(RuntimeError, match="Connection is not active"):
        connection.send({"path": "/rest/api/3/myself"})


def test_jira_connection_sends_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"accountId": "test-user"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.jira.urlopen",
        fake_urlopen,
    )

    connection = JiraConnection(
        "test-token",
        base_url="https://example.atlassian.net",
        email="user@example.com",
    )
    connection.connect()

    result = connection.send({"path": "/rest/api/3/myself"})

    request = request_holder["request"]

    assert request.full_url == (
        "https://example.atlassian.net/rest/api/3/myself"
    )
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request.get_header("X-bindai-jira-email") == "user@example.com"
    assert request_holder["timeout"] == 10.0
    assert result == {
        "status_code": 200,
        "body": '{"accountId": "test-user"}',
    }


def test_jira_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 201
    response.read.return_value = b'{"id": "10001"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.jira.urlopen",
        fake_urlopen,
    )

    connection = JiraConnection(
        "test-token",
        base_url="https://example.atlassian.net",
    )
    connection.connect()

    result = connection.send(
        {
            "path": "/rest/api/3/issue",
            "method": "POST",
            "body": {
                "fields": {
                    "summary": "Hello from BindAI",
                    "project": {"key": "TEST"},
                }
            },
        }
    )

    request = request_holder["request"]

    assert request.full_url == (
        "https://example.atlassian.net/rest/api/3/issue"
    )
    assert request.method == "POST"
    assert request.data == (
        b'{"fields": {"summary": "Hello from BindAI", '
        b'"project": {"key": "TEST"}}}'
    )
    assert request.get_header("Content-type") == "application/json"
    assert result == {
        "status_code": 201,
        "body": '{"id": "10001"}',
    }
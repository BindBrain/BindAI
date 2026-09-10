from unittest.mock import MagicMock

import pytest
from bindai_connections import GitHubConnection


def test_github_connection_lifecycle():
    connection = GitHubConnection("test-token")

    assert connection.name == "github"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_github_connection_rejects_empty_token():
    with pytest.raises(ValueError, match="GitHub token cannot be empty"):
        GitHubConnection("")


def test_github_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="GitHub timeout must be greater than zero",
    ):
        GitHubConnection("test-token", timeout=0)


def test_github_connection_rejects_inactive_send():
    connection = GitHubConnection("test-token")

    with pytest.raises(RuntimeError, match="Connection is not active"):
        connection.send({"path": "/user"})


def test_github_connection_sends_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"login": "bindai"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.github.urlopen",
        fake_urlopen,
    )

    connection = GitHubConnection("test-token")
    connection.connect()

    result = connection.send({"path": "/user"})

    request = request_holder["request"]

    assert request.full_url == "https://api.github.com/user"
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/vnd.github+json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request.get_header("X-github-api-version") == "2022-11-28"
    assert request_holder["timeout"] == 10.0
    assert result == {
        "status_code": 200,
        "body": '{"login": "bindai"}',
    }


def test_github_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 201
    response.read.return_value = b'{"id": 123}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.github.urlopen",
        fake_urlopen,
    )

    connection = GitHubConnection("test-token")
    connection.connect()

    result = connection.send(
        {
            "path": "/repos/example/project/issues",
            "method": "POST",
            "body": {"title": "Hello from BindAI"},
        }
    )

    request = request_holder["request"]

    assert request.full_url == ("https://api.github.com/repos/example/project/issues")
    assert request.method == "POST"
    assert request.data == b'{"title": "Hello from BindAI"}'
    assert request.get_header("Content-type") == "application/json"
    assert result == {
        "status_code": 201,
        "body": '{"id": 123}',
    }

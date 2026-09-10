from unittest.mock import MagicMock

import pytest
from bindai_connections import SlackConnection


def test_slack_connection_lifecycle():
    connection = SlackConnection("test-token")

    assert connection.name == "slack"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_slack_connection_rejects_empty_token():
    with pytest.raises(ValueError, match="Slack token cannot be empty"):
        SlackConnection("")


def test_slack_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Slack timeout must be greater than zero",
    ):
        SlackConnection("test-token", timeout=0)


def test_slack_connection_rejects_inactive_send():
    connection = SlackConnection("test-token")

    with pytest.raises(RuntimeError, match="Connection is not active"):
        connection.send({"path": "/auth.test"})


def test_slack_connection_sends_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"ok": true}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.slack.urlopen",
        fake_urlopen,
    )

    connection = SlackConnection("test-token")
    connection.connect()

    result = connection.send(
        {
            "path": "/auth.test",
            "method": "POST",
        }
    )

    request = request_holder["request"]

    assert request.full_url == "https://slack.com/api/auth.test"
    assert request.method == "POST"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request_holder["timeout"] == 10.0
    assert result == {
        "status_code": 200,
        "body": '{"ok": true}',
    }


def test_slack_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"ok": true}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.slack.urlopen",
        fake_urlopen,
    )

    connection = SlackConnection("test-token")
    connection.connect()

    result = connection.send(
        {
            "path": "/chat.postMessage",
            "method": "POST",
            "body": {
                "channel": "#general",
                "text": "Hello from BindAI",
            },
        }
    )

    request = request_holder["request"]

    assert request.full_url == "https://slack.com/api/chat.postMessage"
    assert request.method == "POST"
    assert request.data == (b'{"channel": "#general", "text": "Hello from BindAI"}')
    assert request.get_header("Content-type") == "application/json"
    assert result == {
        "status_code": 200,
        "body": '{"ok": true}',
    }

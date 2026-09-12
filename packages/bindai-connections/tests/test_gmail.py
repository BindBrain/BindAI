from unittest.mock import MagicMock

import pytest
from bindai_connections.gmail import GmailConnection


def test_gmail_connection_lifecycle():
    connection = GmailConnection("test-token")

    assert connection.name == "gmail"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_gmail_connection_rejects_empty_token():
    with pytest.raises(
        ValueError,
        match="Gmail token cannot be empty",
    ):
        GmailConnection("")


def test_gmail_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Gmail timeout must be greater than zero",
    ):
        GmailConnection("test-token", timeout=0)


def test_gmail_connection_rejects_inactive_send():
    connection = GmailConnection("test-token")

    with pytest.raises(RuntimeError, match="Connection is not active"):
        connection.send({"path": "/me/profile"})


def test_gmail_connection_sends_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"emailAddress": "test@example.com"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.gmail.urlopen",
        fake_urlopen,
    )

    connection = GmailConnection("test-token")
    connection.connect()

    result = connection.send({"path": "/me/profile"})

    request = request_holder["request"]

    assert request.full_url == "https://gmail.googleapis.com/gmail/v1/users/me/profile"
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request_holder["timeout"] == 10.0
    assert result == {
        "status_code": 200,
        "body": '{"emailAddress": "test@example.com"}',
    }


def test_gmail_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"id": "message-id"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.gmail.urlopen",
        fake_urlopen,
    )

    connection = GmailConnection("test-token")
    connection.connect()

    result = connection.send(
        {
            "path": "/me/messages/send",
            "method": "POST",
            "body": {
                "raw": "base64url-encoded-message",
            },
        }
    )

    request = request_holder["request"]

    assert request.full_url == "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
    assert request.method == "POST"
    assert request.data == (b'{"raw": "base64url-encoded-message"}')
    assert request.get_header("Content-type") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert result == {
        "status_code": 200,
        "body": '{"id": "message-id"}',
    }

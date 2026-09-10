from unittest.mock import MagicMock

import pytest
from bindai_connections import ResendConnection


def test_resend_connection_lifecycle():
    connection = ResendConnection(
        "test-api-key",
    )

    assert connection.name == "resend"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_resend_connection_rejects_empty_api_key():
    with pytest.raises(
        ValueError,
        match="Resend API key cannot be empty",
    ):
        ResendConnection("")


def test_resend_connection_rejects_empty_base_url():
    with pytest.raises(
        ValueError,
        match="Resend base URL cannot be empty",
    ):
        ResendConnection(
            "test-api-key",
            base_url="",
        )


def test_resend_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Resend timeout must be greater than zero",
    ):
        ResendConnection(
            "test-api-key",
            timeout=0,
        )


def test_resend_connection_rejects_inactive_send():
    connection = ResendConnection(
        "test-api-key",
    )

    with pytest.raises(
        RuntimeError,
        match="Connection is not active",
    ):
        connection.send(
            {
                "path": "/emails",
            }
        )


def test_resend_connection_sends_post_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"id": "email-123"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.resend.urlopen",
        fake_urlopen,
    )

    connection = ResendConnection(
        "test-api-key",
        base_url="https://api.resend.com",
    )
    connection.connect()

    result = connection.send(
        {
            "path": "/emails",
            "method": "POST",
            "body": {
                "from": "hello@example.com",
                "to": ["user@example.com"],
                "subject": "Hello from BindAI",
                "html": "<p>Hello!</p>",
            },
        }
    )

    request = request_holder["request"]

    assert request.full_url == "https://api.resend.com/emails"
    assert request.method == "POST"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-api-key"
    assert request.get_header("Content-type") == "application/json"
    assert request_holder["timeout"] == 10.0

    assert request.data == (
        b'{"from": "hello@example.com", '
        b'"to": ["user@example.com"], '
        b'"subject": "Hello from BindAI", '
        b'"html": "<p>Hello!</p>"}'
    )

    assert result == {
        "status_code": 200,
        "body": '{"id": "email-123"}',
    }


def test_resend_connection_sends_custom_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"data": []}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.resend.urlopen",
        fake_urlopen,
    )

    connection = ResendConnection(
        "test-api-key",
        base_url="https://example.resend.test/v1",
    )
    connection.connect()

    result = connection.send(
        {
            "path": "/domains",
            "method": "GET",
        }
    )

    request = request_holder["request"]

    assert request.full_url == ("https://example.resend.test/v1/domains")
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-api-key"
    assert request.data is None

    assert result == {
        "status_code": 200,
        "body": '{"data": []}',
    }

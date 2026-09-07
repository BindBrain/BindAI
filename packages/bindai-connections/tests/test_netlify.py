from unittest.mock import MagicMock

import pytest

from bindai_connections import NetlifyConnection


def test_netlify_connection_lifecycle():
    connection = NetlifyConnection("test-token")

    assert connection.name == "netlify"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_netlify_connection_rejects_empty_token():
    with pytest.raises(
        ValueError,
        match="Netlify token cannot be empty",
    ):
        NetlifyConnection("")


def test_netlify_connection_rejects_empty_base_url():
    with pytest.raises(
        ValueError,
        match="Netlify base URL cannot be empty",
    ):
        NetlifyConnection(
            "test-token",
            base_url="",
        )


def test_netlify_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Netlify timeout must be greater than zero",
    ):
        NetlifyConnection(
            "test-token",
            timeout=0,
        )


def test_netlify_connection_rejects_inactive_send():
    connection = NetlifyConnection("test-token")

    with pytest.raises(
        RuntimeError,
        match="Connection is not active",
    ):
        connection.send(
            {
                "path": "/user",
            }
        )


def test_netlify_connection_sends_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"id": "user-123"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.netlify.urlopen",
        fake_urlopen,
    )

    connection = NetlifyConnection(
        "test-token",
        base_url="https://api.netlify.com/api/v1",
    )
    connection.connect()

    result = connection.send(
        {
            "path": "/user",
        }
    )

    request = request_holder["request"]

    assert request.full_url == (
        "https://api.netlify.com/api/v1/user"
    )
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request_holder["timeout"] == 10.0

    assert result == {
        "status_code": 200,
        "body": '{"id": "user-123"}',
    }


def test_netlify_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 201
    response.read.return_value = b'{"id": "site-123"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.netlify.urlopen",
        fake_urlopen,
    )

    connection = NetlifyConnection(
        "test-token",
        base_url="https://api.netlify.com/api/v1",
    )
    connection.connect()

    result = connection.send(
        {
            "path": "/sites",
            "method": "POST",
            "body": {
                "name": "bindai-app",
            },
        }
    )

    request = request_holder["request"]

    assert request.full_url == (
        "https://api.netlify.com/api/v1/sites"
    )
    assert request.method == "POST"
    assert request.data == b'{"name": "bindai-app"}'
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request.get_header("Content-type") == "application/json"

    assert result == {
        "status_code": 201,
        "body": '{"id": "site-123"}',
    }
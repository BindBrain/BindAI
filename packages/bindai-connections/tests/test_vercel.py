from unittest.mock import MagicMock

import pytest
from bindai_connections import VercelConnection


def test_vercel_connection_lifecycle():
    connection = VercelConnection(
        "test-token",
    )

    assert connection.name == "vercel"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_vercel_connection_rejects_empty_token():
    with pytest.raises(
        ValueError,
        match="Vercel token cannot be empty",
    ):
        VercelConnection("")


def test_vercel_connection_rejects_empty_base_url():
    with pytest.raises(
        ValueError,
        match="Vercel base URL cannot be empty",
    ):
        VercelConnection(
            "test-token",
            base_url="",
        )


def test_vercel_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Vercel timeout must be greater than zero",
    ):
        VercelConnection(
            "test-token",
            timeout=0,
        )


def test_vercel_connection_rejects_inactive_send():
    connection = VercelConnection(
        "test-token",
    )

    with pytest.raises(
        RuntimeError,
        match="Connection is not active",
    ):
        connection.send(
            {
                "path": "/v2/user",
            }
        )


def test_vercel_connection_sends_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"user": {"id": "user-123"}}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.vercel.urlopen",
        fake_urlopen,
    )

    connection = VercelConnection(
        "test-token",
        base_url="https://api.vercel.com",
    )
    connection.connect()

    result = connection.send(
        {
            "path": "/v2/user",
        }
    )

    request = request_holder["request"]

    assert request.full_url == "https://api.vercel.com/v2/user"
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request_holder["timeout"] == 10.0

    assert result == {
        "status_code": 200,
        "body": '{"user": {"id": "user-123"}}',
    }


def test_vercel_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"id": "deployment-123"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.vercel.urlopen",
        fake_urlopen,
    )

    connection = VercelConnection(
        "test-token",
        base_url="https://api.vercel.com",
    )
    connection.connect()

    result = connection.send(
        {
            "path": "/v13/deployments",
            "method": "POST",
            "body": {
                "name": "bindai-app",
                "target": "production",
            },
        }
    )

    request = request_holder["request"]

    assert request.full_url == ("https://api.vercel.com/v13/deployments")
    assert request.method == "POST"
    assert request.data == (b'{"name": "bindai-app", "target": "production"}')
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request.get_header("Content-type") == "application/json"

    assert result == {
        "status_code": 200,
        "body": '{"id": "deployment-123"}',
    }

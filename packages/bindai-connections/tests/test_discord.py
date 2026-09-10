from unittest.mock import MagicMock

import pytest
from bindai_connections import DiscordConnection


def test_discord_connection_lifecycle():
    connection = DiscordConnection(
        "test-token",
    )

    assert connection.name == "discord"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_discord_connection_rejects_empty_token():
    with pytest.raises(
        ValueError,
        match="Discord token cannot be empty",
    ):
        DiscordConnection("")


def test_discord_connection_rejects_empty_base_url():
    with pytest.raises(
        ValueError,
        match="Discord base URL cannot be empty",
    ):
        DiscordConnection(
            "test-token",
            base_url="",
        )


def test_discord_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Discord timeout must be greater than zero",
    ):
        DiscordConnection(
            "test-token",
            timeout=0,
        )


def test_discord_connection_rejects_inactive_send():
    connection = DiscordConnection(
        "test-token",
    )

    with pytest.raises(
        RuntimeError,
        match="Connection is not active",
    ):
        connection.send(
            {
                "path": "/users/@me",
            }
        )


def test_discord_connection_sends_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"id": "123456789"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.discord.urlopen",
        fake_urlopen,
    )

    connection = DiscordConnection(
        "test-token",
        base_url="https://discord.com/api/v10",
    )
    connection.connect()

    result = connection.send(
        {
            "path": "/users/@me",
        }
    )

    request = request_holder["request"]

    assert request.full_url == ("https://discord.com/api/v10/users/@me")
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bot test-token"
    assert request_holder["timeout"] == 10.0

    assert result == {
        "status_code": 200,
        "body": '{"id": "123456789"}',
    }


def test_discord_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 204
    response.read.return_value = b""
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.discord.urlopen",
        fake_urlopen,
    )

    connection = DiscordConnection(
        "test-token",
        base_url="https://discord.com/api/v10",
    )
    connection.connect()

    result = connection.send(
        {
            "path": "/channels/123456789/messages",
            "method": "POST",
            "body": {
                "content": "Hello from BindAI",
            },
        }
    )

    request = request_holder["request"]

    assert request.full_url == ("https://discord.com/api/v10/channels/123456789/messages")
    assert request.method == "POST"
    assert request.data == (b'{"content": "Hello from BindAI"}')
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bot test-token"
    assert request.get_header("Content-type") == "application/json"

    assert result == {
        "status_code": 204,
        "body": "",
    }

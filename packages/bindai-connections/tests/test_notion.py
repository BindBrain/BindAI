from unittest.mock import MagicMock

import pytest

from bindai_connections import NotionConnection


def test_notion_connection_lifecycle():
    connection = NotionConnection("test-token")

    assert connection.name == "notion"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_notion_connection_rejects_empty_token():
    with pytest.raises(ValueError, match="Notion token cannot be empty"):
        NotionConnection("")


def test_notion_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Notion timeout must be greater than zero",
    ):
        NotionConnection("test-token", timeout=0)


def test_notion_connection_rejects_inactive_send():
    connection = NotionConnection("test-token")

    with pytest.raises(RuntimeError, match="Connection is not active"):
        connection.send({"path": "/users/me"})


def test_notion_connection_sends_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"object": "user"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.notion.urlopen",
        fake_urlopen,
    )

    connection = NotionConnection("test-token")
    connection.connect()

    result = connection.send({"path": "/users/me"})

    request = request_holder["request"]

    assert request.full_url == "https://api.notion.com/v1/users/me"
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request.get_header("Notion-version") == "2022-06-28"
    assert request_holder["timeout"] == 10.0
    assert result == {
        "status_code": 200,
        "body": '{"object": "user"}',
    }


def test_notion_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"object": "page"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.notion.urlopen",
        fake_urlopen,
    )

    connection = NotionConnection("test-token")
    connection.connect()

    result = connection.send(
        {
            "path": "/pages",
            "method": "POST",
            "body": {
                "parent": {"page_id": "test-page"},
                "properties": {},
            },
        }
    )

    request = request_holder["request"]

    assert request.full_url == "https://api.notion.com/v1/pages"
    assert request.method == "POST"
    assert request.data == (
        b'{"parent": {"page_id": "test-page"}, "properties": {}}'
    )
    assert request.get_header("Content-type") == "application/json"
    assert result == {
        "status_code": 200,
        "body": '{"object": "page"}',
    }
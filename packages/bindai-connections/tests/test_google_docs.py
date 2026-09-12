from unittest.mock import MagicMock

import pytest
from bindai_connections.google_docs import GoogleDocsConnection


def test_google_docs_connection_lifecycle():
    connection = GoogleDocsConnection("test-token")

    assert connection.name == "google_docs"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_google_docs_connection_rejects_empty_token():
    with pytest.raises(
        ValueError,
        match="Google Docs token cannot be empty",
    ):
        GoogleDocsConnection("")


def test_google_docs_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Google Docs timeout must be greater than zero",
    ):
        GoogleDocsConnection("test-token", timeout=0)


def test_google_docs_connection_rejects_inactive_send():
    connection = GoogleDocsConnection("test-token")

    with pytest.raises(RuntimeError, match="Connection is not active"):
        connection.send({"path": "/test-document"})


def test_google_docs_connection_sends_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"documentId": "test-id"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.google_docs.urlopen",
        fake_urlopen,
    )

    connection = GoogleDocsConnection("test-token")
    connection.connect()

    result = connection.send({"path": "/test-document"})

    request = request_holder["request"]

    assert (
        request.full_url == "https://docs.googleapis.com/v1/documents/"
        "test-document?access_token=test-token"
    )
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request_holder["timeout"] == 10.0
    assert result == {
        "status_code": 200,
        "body": '{"documentId": "test-id"}',
    }


def test_google_docs_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"replies": []}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.google_docs.urlopen",
        fake_urlopen,
    )

    connection = GoogleDocsConnection("test-token")
    connection.connect()

    result = connection.send(
        {
            "path": "/test-document:batchUpdate",
            "method": "POST",
            "body": {
                "requests": [],
            },
        }
    )

    request = request_holder["request"]

    assert (
        request.full_url == "https://docs.googleapis.com/v1/documents/"
        "test-document:batchUpdate?access_token=test-token"
    )
    assert request.method == "POST"
    assert request.data == b'{"requests": []}'
    assert request.get_header("Content-type") == "application/json"
    assert result == {
        "status_code": 200,
        "body": '{"replies": []}',
    }

from unittest.mock import MagicMock

import pytest
from bindai_connections.google_drive import GoogleDriveConnection


def test_google_drive_connection_lifecycle():
    connection = GoogleDriveConnection("test-token")

    assert connection.name == "google_drive"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_google_drive_connection_rejects_empty_token():
    with pytest.raises(
        ValueError,
        match="Google Drive token cannot be empty",
    ):
        GoogleDriveConnection("")


def test_google_drive_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Google Drive timeout must be greater than zero",
    ):
        GoogleDriveConnection("test-token", timeout=0)


def test_google_drive_connection_rejects_inactive_send():
    connection = GoogleDriveConnection("test-token")

    with pytest.raises(RuntimeError, match="Connection is not active"):
        connection.send({"path": "/files"})


def test_google_drive_connection_sends_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"files": []}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.google_drive.urlopen",
        fake_urlopen,
    )

    connection = GoogleDriveConnection("test-token")
    connection.connect()

    result = connection.send({"path": "/files"})

    request = request_holder["request"]

    assert request.full_url == ("https://www.googleapis.com/drive/v3/files")
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert request_holder["timeout"] == 10.0
    assert result == {
        "status_code": 200,
        "body": '{"files": []}',
    }


def test_google_drive_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"id": "file-id"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.google_drive.urlopen",
        fake_urlopen,
    )

    connection = GoogleDriveConnection("test-token")
    connection.connect()

    result = connection.send(
        {
            "path": "/files",
            "method": "POST",
            "body": {
                "name": "BindAI file",
            },
        }
    )

    request = request_holder["request"]

    assert request.full_url == ("https://www.googleapis.com/drive/v3/files")
    assert request.method == "POST"
    assert request.data == b'{"name": "BindAI file"}'
    assert request.get_header("Content-type") == "application/json"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert result == {
        "status_code": 200,
        "body": '{"id": "file-id"}',
    }

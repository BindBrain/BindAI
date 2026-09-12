from unittest.mock import MagicMock

import pytest
from bindai_connections.google_sheets import GoogleSheetsConnection


def test_google_sheets_connection_lifecycle():
    connection = GoogleSheetsConnection("test-token")

    assert connection.name == "google_sheets"
    assert not connection.is_connected()

    connection.connect()
    assert connection.is_connected()

    connection.disconnect()
    assert not connection.is_connected()


def test_google_sheets_connection_rejects_empty_token():
    with pytest.raises(
        ValueError,
        match="Google Sheets token cannot be empty",
    ):
        GoogleSheetsConnection("")


def test_google_sheets_connection_rejects_invalid_timeout():
    with pytest.raises(
        ValueError,
        match="Google Sheets timeout must be greater than zero",
    ):
        GoogleSheetsConnection("test-token", timeout=0)


def test_google_sheets_connection_rejects_inactive_send():
    connection = GoogleSheetsConnection("test-token")

    with pytest.raises(RuntimeError, match="Connection is not active"):
        connection.send({"path": "/test-spreadsheet"})


def test_google_sheets_connection_sends_get_request(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"spreadsheetId": "test-id"}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.google_sheets.urlopen",
        fake_urlopen,
    )

    connection = GoogleSheetsConnection("test-token")
    connection.connect()

    result = connection.send({"path": "/test-spreadsheet"})

    request = request_holder["request"]

    assert (
        request.full_url == "https://sheets.googleapis.com/v4/spreadsheets/"
        "test-spreadsheet?access_token=test-token"
    )
    assert request.method == "GET"
    assert request.get_header("Accept") == "application/json"
    assert request_holder["timeout"] == 10.0
    assert result == {
        "status_code": 200,
        "body": '{"spreadsheetId": "test-id"}',
    }


def test_google_sheets_connection_sends_json_body(monkeypatch):
    response = MagicMock()
    response.status = 200
    response.read.return_value = b'{"updatedRows": 1}'
    response.__enter__.return_value = response
    response.__exit__.return_value = None

    request_holder = {}

    def fake_urlopen(request, timeout):
        request_holder["request"] = request
        request_holder["timeout"] = timeout
        return response

    monkeypatch.setattr(
        "bindai_connections.google_sheets.urlopen",
        fake_urlopen,
    )

    connection = GoogleSheetsConnection("test-token")
    connection.connect()

    result = connection.send(
        {
            "path": "/test-spreadsheet/values/Sheet1!A1",
            "method": "PUT",
            "body": {
                "values": [["Hello from BindAI"]],
            },
        }
    )

    request = request_holder["request"]

    assert (
        request.full_url == "https://sheets.googleapis.com/v4/spreadsheets/"
        "test-spreadsheet/values/Sheet1!A1?access_token=test-token"
    )
    assert request.method == "PUT"
    assert request.data == (b'{"values": [["Hello from BindAI"]]}')
    assert request.get_header("Content-type") == "application/json"
    assert result == {
        "status_code": 200,
        "body": '{"updatedRows": 1}',
    }

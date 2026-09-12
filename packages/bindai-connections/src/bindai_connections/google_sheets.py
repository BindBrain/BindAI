from __future__ import annotations

import json
from urllib.request import Request, urlopen

from .connection import Connection


class GoogleSheetsConnection(Connection):
    """HTTP connection for the Google Sheets API."""

    def __init__(
        self,
        token: str,
        *,
        base_url: str = "https://sheets.googleapis.com/v4/spreadsheets",
        timeout: float = 10.0,
    ) -> None:
        if not token.strip():
            raise ValueError("Google Sheets token cannot be empty.")
        if not base_url.strip():
            raise ValueError("Google Sheets base URL cannot be empty.")
        if timeout <= 0:
            raise ValueError("Google Sheets timeout must be greater than zero.")

        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._connected = False

    @property
    def name(self) -> str:
        return "google_sheets"

    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def send(self, payload: dict) -> dict:
        if not self._connected:
            raise RuntimeError("Connection is not active.")

        path = payload.get("path", "")
        method = payload.get("method", "GET").upper()
        body = payload.get("body")

        url = f"{self.base_url}/{path.lstrip('/')}"

        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}access_token={self.token}"

        headers = {
            "Accept": "application/json",
        }

        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = Request(
            url,
            data=data,
            headers=headers,
            method=method,
        )

        with urlopen(request, timeout=self.timeout) as response:
            response_body = response.read().decode("utf-8")

            return {
                "status_code": response.status,
                "body": response_body,
            }

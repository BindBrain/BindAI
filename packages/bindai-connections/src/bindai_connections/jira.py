from __future__ import annotations

import json
from urllib.request import Request, urlopen

from .connection import Connection


class JiraConnection(Connection):
    """HTTP connection for the Jira REST API."""

    def __init__(
        self,
        token: str,
        *,
        base_url: str,
        email: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        if not token.strip():
            raise ValueError("Jira token cannot be empty.")
        if not base_url.strip():
            raise ValueError("Jira base URL cannot be empty.")
        if timeout <= 0:
            raise ValueError("Jira timeout must be greater than zero.")

        self.token = token
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.timeout = timeout
        self._connected = False

    @property
    def name(self) -> str:
        return "jira"

    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def send(self, payload: dict) -> dict:
        if not self._connected:
            raise RuntimeError("Connection is not active.")

        path = payload.get("path", "/rest/api/3/myself")
        method = payload.get("method", "GET").upper()
        body = payload.get("body")

        url = f"{self.base_url}/{path.lstrip('/')}"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        if self.email:
            headers["X-BindAI-Jira-Email"] = self.email

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

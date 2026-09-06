from __future__ import annotations

import json
from urllib.request import Request, urlopen

from .connection import Connection


class WebhookConnection(Connection):
    """HTTP webhook connection for sending JSON payloads."""

    def __init__(self, url: str, *, timeout: float = 10.0) -> None:
        if not url.strip():
            raise ValueError("Webhook URL cannot be empty.")
        if timeout <= 0:
            raise ValueError("Webhook timeout must be greater than zero.")

        self.url = url
        self.timeout = timeout
        self._connected = False

    @property
    def name(self) -> str:
        return "webhook"

    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def send(self, payload) -> dict:
        if not self._connected:
            raise RuntimeError("Connection is not active.")

        body = json.dumps(payload).encode("utf-8")
        request = Request(
            self.url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request, timeout=self.timeout) as response:
            return {
                "status_code": response.status,
                "body": response.read().decode("utf-8"),
            }

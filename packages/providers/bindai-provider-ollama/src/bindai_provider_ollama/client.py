from __future__ import annotations

from bindai_core import ProviderConfiguration
from ollama import Client


class OllamaClient:
    def __init__(self, configuration: ProviderConfiguration) -> None:
        self._configuration = configuration
        self._client: Client | None = None

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(
                host=self._configuration.endpoint,
            )

        return self._client

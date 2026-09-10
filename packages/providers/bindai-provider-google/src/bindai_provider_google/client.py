from __future__ import annotations

from bindai_core import ProviderConfiguration
from google import genai


class GoogleClient:
    def __init__(self, configuration: ProviderConfiguration) -> None:
        self._configuration = configuration
        self._client: genai.Client | None = None

    @property
    def client(self) -> genai.Client:
        if self._client is None:
            self._client = genai.Client(
                api_key=self._configuration.api_key,
            )
        return self._client

from __future__ import annotations

from bindai_core import ProviderConfiguration
from groq import Groq


class GroqClient:
    def __init__(self, configuration: ProviderConfiguration) -> None:
        self._configuration = configuration
        self._client: Groq | None = None

    @property
    def client(self) -> Groq:
        if self._client is None:
            self._client = Groq(
                api_key=self._configuration.api_key,
            )
        return self._client

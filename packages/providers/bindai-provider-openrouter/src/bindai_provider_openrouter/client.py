from __future__ import annotations

from openai import OpenAI

from bindai_core import ProviderConfiguration


class OpenRouterClient:
    def __init__(self, configuration: ProviderConfiguration) -> None:
        self._configuration = configuration
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI(
                api_key=self._configuration.api_key,
                base_url=self._configuration.endpoint,
            )

        return self._client
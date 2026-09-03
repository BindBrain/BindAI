from __future__ import annotations

from anthropic import Anthropic
from bindai_core import ProviderConfiguration


class AnthropicClient:
    def __init__(self, configuration: ProviderConfiguration) -> None:
        self._configuration = configuration
        self._client: Anthropic | None = None

    @property
    def client(self) -> Anthropic:
        if self._client is None:
            self._client = Anthropic(
                api_key=self._configuration.api_key,
                base_url=self._configuration.endpoint,
                timeout=self._configuration.timeout,
                default_headers=self._configuration.headers,
            )
        return self._client

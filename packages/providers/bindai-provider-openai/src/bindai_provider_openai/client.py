from __future__ import annotations

from bindai_core import ProviderConfiguration
from openai import OpenAI


class OpenAIClient:
    """
    Thin wrapper around the official OpenAI SDK.

    The OpenAI client is created lazily so the provider
    can be constructed before credentials are available.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
    ) -> None:
        self._configuration = configuration
        self._client: OpenAI | None = None

    @property
    def client(
        self,
    ) -> OpenAI:

        if self._client is None:
            self._client = OpenAI(
                api_key=self._configuration.api_key,
                base_url=self._configuration.endpoint,
                organization=self._configuration.organization,
            )

        return self._client
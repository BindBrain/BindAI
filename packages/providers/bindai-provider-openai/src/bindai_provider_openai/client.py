from __future__ import annotations

from openai import OpenAI

from bindai_core import ProviderConfiguration


class OpenAIClient:
    """
    Thin wrapper around the official OpenAI SDK.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
    ):

        self._client = OpenAI(
            api_key=configuration.api_key,
            base_url=configuration.endpoint,
            organization=configuration.organization,
        )

    @property
    def client(self) -> OpenAI:
        return self._client
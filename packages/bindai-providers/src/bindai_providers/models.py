from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ProviderConfiguration:
    """
    Provider configuration.
    """

    api_key: str | None = None

    endpoint: str | None = None

    organization: str | None = None

    model: str = ""


@dataclass(slots=True)
class ProviderCapabilities:
    """
    Provider capabilities.
    """

    streaming: bool = True

    tools: bool = True

    structured_output: bool = True

    images: bool = False

    embeddings: bool = False
from dataclasses import dataclass


@dataclass(slots=True)
class ProviderConfiguration:
    """
    Configuration for an AI provider.
    """

    api_key: str | None = None

    endpoint: str | None = None

    model: str | None = None

    organization: str | None = None

    timeout: int = 60
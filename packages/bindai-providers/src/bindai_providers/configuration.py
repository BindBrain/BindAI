from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ProviderConfiguration:
    """
    Common configuration shared by all providers.
    """

    api_key: str | None = None

    endpoint: str | None = None

    organization: str | None = None

    model: str | None = None

    timeout: int = 60

    headers: dict[str, str] = field(
        default_factory=dict,
    )
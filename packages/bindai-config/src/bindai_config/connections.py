from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProviderConnection:
    """
    Describes how a provider connection obtains its runtime values.

    This metadata does not contain secrets. It only describes the
    environment variables that can currently provide them.
    """

    provider: str
    api_key_env: str | None = None
    endpoint_env: str | None = None
    organization_env: str | None = None


_PROVIDER_CONNECTIONS = {
    "openai": ProviderConnection(
        provider="openai",
        api_key_env="OPENAI_API_KEY",
        endpoint_env="OPENAI_BASE_URL",
        organization_env="OPENAI_ORGANIZATION",
    ),
    "anthropic": ProviderConnection(
        provider="anthropic",
        api_key_env="ANTHROPIC_API_KEY",
    ),
    "google": ProviderConnection(
        provider="google",
        api_key_env="GEMINI_API_KEY",
    ),
    "groq": ProviderConnection(
        provider="groq",
        api_key_env="GROQ_API_KEY",
    ),
    "ollama": ProviderConnection(
        provider="ollama",
        endpoint_env="OLLAMA_HOST",
    ),
    "openrouter": ProviderConnection(
        provider="openrouter",
        api_key_env="OPENROUTER_API_KEY",
    ),
}


def get_provider_connection(provider: str) -> ProviderConnection:
    """
    Return connection metadata for a provider.
    """
    provider_name = provider.lower()

    try:
        return _PROVIDER_CONNECTIONS[provider_name]
    except KeyError as exc:
        raise KeyError(
            f'Unknown provider "{provider}".',
        ) from exc


def list_provider_connections() -> tuple[ProviderConnection, ...]:
    """
    Return all known provider connection definitions.
    """
    return tuple(_PROVIDER_CONNECTIONS.values())

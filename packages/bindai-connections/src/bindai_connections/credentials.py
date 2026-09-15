from __future__ import annotations

from abc import ABC, abstractmethod


class ProviderCredentialStore(ABC):
    """Store and retrieve credentials for AI model providers."""

    @abstractmethod
    def set(self, provider: str, credential: str) -> None:
        """Store a credential for a provider."""
        ...

    @abstractmethod
    def get(self, provider: str) -> str | None:
        """Return a provider credential, or None when unavailable."""
        ...

    @abstractmethod
    def delete(self, provider: str) -> None:
        """Delete a provider credential if it exists."""
        ...

    @abstractmethod
    def exists(self, provider: str) -> bool:
        """Return whether a credential exists for a provider."""
        ...

    @abstractmethod
    def list(self) -> list[str]:
        """Return provider names with stored credentials."""
        ...


class InMemoryProviderCredentialStore(ProviderCredentialStore):
    """In-memory credential store used for testing and local composition."""

    def __init__(self) -> None:
        self._credentials: dict[str, str] = {}

    def set(self, provider: str, credential: str) -> None:
        provider_name = self._normalize_provider(provider)

        if not credential:
            raise ValueError("Credential cannot be empty.")

        self._credentials[provider_name] = credential

    def get(self, provider: str) -> str | None:
        provider_name = self._normalize_provider(provider)
        return self._credentials.get(provider_name)

    def delete(self, provider: str) -> None:
        provider_name = self._normalize_provider(provider)
        self._credentials.pop(provider_name, None)

    def exists(self, provider: str) -> bool:
        provider_name = self._normalize_provider(provider)
        return provider_name in self._credentials

    def list(self) -> list[str]:
        return list(self._credentials)

    @staticmethod
    def _normalize_provider(provider: str) -> str:
        provider_name = provider.strip().lower()

        if not provider_name:
            raise ValueError("Provider cannot be empty.")

        return provider_name
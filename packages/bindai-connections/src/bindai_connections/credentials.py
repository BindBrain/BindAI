from __future__ import annotations

from abc import ABC, abstractmethod


class ProviderCredentialStore(ABC):
    """Store and retrieve credentials for named BindAI connections."""

    @abstractmethod
    def set(self, connection_name: str, credential: str) -> None:
        """Store a credential for a connection."""
        ...

    @abstractmethod
    def get(self, connection_name: str) -> str | None:
        """Return a connection credential, or None when unavailable."""
        ...

    @abstractmethod
    def delete(self, connection_name: str) -> None:
        """Delete a connection credential if it exists."""
        ...

    @abstractmethod
    def exists(self, connection_name: str) -> bool:
        """Return whether a credential exists for a connection."""
        ...

    @abstractmethod
    def list(self) -> list[str]:
        """Return connection names with stored credentials."""
        ...


class InMemoryProviderCredentialStore(ProviderCredentialStore):
    """In-memory credential store used for testing and local composition."""

    def __init__(self) -> None:
        self._credentials: dict[str, str] = {}

    def set(self, connection_name: str, credential: str) -> None:
        normalized_name = self._normalize_connection_name(
            connection_name,
        )

        if not credential:
            raise ValueError("Credential cannot be empty.")

        self._credentials[normalized_name] = credential

    def get(self, connection_name: str) -> str | None:
        normalized_name = self._normalize_connection_name(
            connection_name,
        )
        return self._credentials.get(normalized_name)

    def delete(self, connection_name: str) -> None:
        normalized_name = self._normalize_connection_name(
            connection_name,
        )
        self._credentials.pop(normalized_name, None)

    def exists(self, connection_name: str) -> bool:
        normalized_name = self._normalize_connection_name(
            connection_name,
        )
        return normalized_name in self._credentials

    def list(self) -> list[str]:
        return list(self._credentials)

    @staticmethod
    def _normalize_connection_name(connection_name: str) -> str:
        normalized_name = connection_name.strip().lower()

        if not normalized_name:
            raise ValueError("Connection name cannot be empty.")

        return normalized_name
from __future__ import annotations

from .credentials import ProviderCredentialStore


class KeyringProviderCredentialStore(ProviderCredentialStore):
    """Store connection credentials using the operating system credential store."""

    SERVICE_NAME = "bindai"

    def __init__(self, service_name: str = SERVICE_NAME) -> None:
        if not service_name.strip():
            raise ValueError("Service name cannot be empty.")

        self._service_name = service_name

    def set(self, connection_name: str, credential: str) -> None:
        self._validate_connection_name(connection_name)
        self._validate_credential(credential)

        self._keyring().set_password(
            self._service_name,
            self._normalize_connection_name(connection_name),
            credential,
        )

    def get(self, connection_name: str) -> str | None:
        normalized_name = self._normalize_connection_name(
            connection_name,
        )

        return self._keyring().get_password(
            self._service_name,
            normalized_name,
        )

    def delete(self, connection_name: str) -> None:
        normalized_name = self._normalize_connection_name(
            connection_name,
        )
        keyring = self._keyring()

        try:
            keyring.delete_password(
                self._service_name,
                normalized_name,
            )
        except keyring.errors.PasswordDeleteError:
            return

    def exists(self, connection_name: str) -> bool:
        return self.get(connection_name) is not None

    def list(self) -> list[str]:
        """
        Return connection names stored by this backend.

        The keyring API does not provide a portable way to enumerate
        credentials, so this backend intentionally does not attempt it.
        """
        return []

    @staticmethod
    def _normalize_connection_name(connection_name: str) -> str:
        normalized_name = connection_name.strip().lower()

        if not normalized_name:
            raise ValueError("Connection name cannot be empty.")

        return normalized_name

    @classmethod
    def _validate_connection_name(cls, connection_name: str) -> None:
        cls._normalize_connection_name(connection_name)

    @staticmethod
    def _validate_credential(credential: str) -> None:
        if not credential:
            raise ValueError("Credential cannot be empty.")

    @staticmethod
    def _keyring():
        try:
            import keyring
        except ImportError as exc:
            raise RuntimeError(
                "The keyring package is required for OS-backed credentials. "
                'Install it with "pip install bindai-connections[credentials]".',
            ) from exc

        return keyring
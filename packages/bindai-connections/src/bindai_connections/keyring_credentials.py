from __future__ import annotations

from .credentials import ProviderCredentialStore


class KeyringProviderCredentialStore(ProviderCredentialStore):
    """Store provider credentials using the operating system credential store."""

    SERVICE_NAME = "bindai"

    def __init__(self, service_name: str = SERVICE_NAME) -> None:
        if not service_name.strip():
            raise ValueError("Service name cannot be empty.")

        self._service_name = service_name

    def set(self, provider: str, credential: str) -> None:
        self._validate_provider(provider)
        self._validate_credential(credential)

        self._keyring().set_password(
            self._service_name,
            self._normalize_provider(provider),
            credential,
        )

    def get(self, provider: str) -> str | None:
        provider_name = self._normalize_provider(provider)

        return self._keyring().get_password(
            self._service_name,
            provider_name,
        )

    def delete(self, provider: str) -> None:
        provider_name = self._normalize_provider(provider)
        keyring = self._keyring()

        try:
            keyring.delete_password(
                self._service_name,
                provider_name,
            )
        except keyring.errors.PasswordDeleteError:
            return

    def exists(self, provider: str) -> bool:
        return self.get(provider) is not None

    def list(self) -> list[str]:
        """
        Return provider names stored by this backend.

        The keyring API does not provide a portable way to enumerate
        credentials, so this backend intentionally does not attempt it.
        """
        return []

    @staticmethod
    def _normalize_provider(provider: str) -> str:
        provider_name = provider.strip().lower()

        if not provider_name:
            raise ValueError("Provider cannot be empty.")

        return provider_name

    @classmethod
    def _validate_provider(cls, provider: str) -> None:
        cls._normalize_provider(provider)

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
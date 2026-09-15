import pytest
from bindai_connections import KeyringProviderCredentialStore


class FakeKeyringErrors:
    class PasswordDeleteError(Exception):
        pass


class FakeKeyring:
    def __init__(self):
        self.values = {}
        self.errors = FakeKeyringErrors

    def set_password(self, service, username, password):
        self.values[(service, username)] = password

    def get_password(self, service, username):
        return self.values.get((service, username))

    def delete_password(self, service, username):
        key = (service, username)

        if key not in self.values:
            raise self.errors.PasswordDeleteError()

        del self.values[key]


@pytest.fixture
def fake_keyring(monkeypatch):
    keyring = FakeKeyring()

    monkeypatch.setattr(
        KeyringProviderCredentialStore,
        "_keyring",
        staticmethod(lambda: keyring),
    )

    return keyring


def test_set_and_get_credential(fake_keyring):
    store = KeyringProviderCredentialStore()

    store.set("openai", "secret-key")

    assert fake_keyring.values[("bindai", "openai")] == "secret-key"
    assert store.get("openai") == "secret-key"


def test_provider_names_are_normalized(fake_keyring):
    store = KeyringProviderCredentialStore()

    store.set("  OpenAI  ", "secret-key")

    assert store.get("OPENAI") == "secret-key"


def test_exists(fake_keyring):
    store = KeyringProviderCredentialStore()

    assert not store.exists("openai")

    store.set("openai", "secret-key")

    assert store.exists("openai")


def test_delete(fake_keyring):
    store = KeyringProviderCredentialStore()

    store.set("openai", "secret-key")
    store.delete("openai")

    assert store.get("openai") is None


def test_delete_missing_credential_is_safe(fake_keyring):
    store = KeyringProviderCredentialStore()

    store.delete("openai")

    assert not store.exists("openai")


def test_list_does_not_expose_credentials(fake_keyring):
    store = KeyringProviderCredentialStore()

    store.set("openai", "secret-key")

    assert store.list() == []


def test_empty_provider_is_rejected(fake_keyring):
    store = KeyringProviderCredentialStore()

    with pytest.raises(ValueError, match="Provider cannot be empty"):
        store.set("", "secret-key")


def test_empty_credential_is_rejected(fake_keyring):
    store = KeyringProviderCredentialStore()

    with pytest.raises(ValueError, match="Credential cannot be empty"):
        store.set("openai", "")


def test_empty_service_name_is_rejected():
    with pytest.raises(ValueError, match="Service name cannot be empty"):
        KeyringProviderCredentialStore("   ")
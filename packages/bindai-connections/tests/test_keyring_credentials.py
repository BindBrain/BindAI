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

    store.set("work", "secret-key")

    assert fake_keyring.values[("bindai", "work")] == "secret-key"
    assert store.get("work") == "secret-key"


def test_connection_names_are_normalized(fake_keyring):
    store = KeyringProviderCredentialStore()

    store.set("  Work  ", "secret-key")

    assert store.get("WORK") == "secret-key"


def test_multiple_connections_keep_independent_credentials(fake_keyring):
    store = KeyringProviderCredentialStore()

    store.set("work", "work-secret")
    store.set("personal", "personal-secret")

    assert fake_keyring.values[("bindai", "work")] == "work-secret"
    assert fake_keyring.values[("bindai", "personal")] == "personal-secret"
    assert store.get("work") == "work-secret"
    assert store.get("personal") == "personal-secret"


def test_exists(fake_keyring):
    store = KeyringProviderCredentialStore()

    assert not store.exists("work")

    store.set("work", "secret-key")

    assert store.exists("work")


def test_delete(fake_keyring):
    store = KeyringProviderCredentialStore()

    store.set("work", "secret-key")
    store.delete("work")

    assert store.get("work") is None


def test_delete_missing_credential_is_safe(fake_keyring):
    store = KeyringProviderCredentialStore()

    store.delete("work")

    assert not store.exists("work")


def test_list_does_not_expose_credentials(fake_keyring):
    store = KeyringProviderCredentialStore()

    store.set("work", "secret-key")

    assert store.list() == []


def test_empty_connection_name_is_rejected(fake_keyring):
    store = KeyringProviderCredentialStore()

    with pytest.raises(
        ValueError,
        match="Connection name cannot be empty",
    ):
        store.set("", "secret-key")


def test_empty_credential_is_rejected(fake_keyring):
    store = KeyringProviderCredentialStore()

    with pytest.raises(
        ValueError,
        match="Credential cannot be empty",
    ):
        store.set("work", "")


def test_empty_service_name_is_rejected():
    with pytest.raises(
        ValueError,
        match="Service name cannot be empty",
    ):
        KeyringProviderCredentialStore("   ")
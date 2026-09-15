import pytest
from bindai_connections import (
    InMemoryProviderCredentialStore,
    ProviderCredentialStore,
)


def test_in_memory_store_implements_provider_credential_store():
    store = InMemoryProviderCredentialStore()

    assert isinstance(store, ProviderCredentialStore)


def test_store_and_get_credential():
    store = InMemoryProviderCredentialStore()

    store.set("work", "secret-key")

    assert store.get("work") == "secret-key"


def test_connection_names_are_case_insensitive():
    store = InMemoryProviderCredentialStore()

    store.set("Work", "secret-key")

    assert store.get("work") == "secret-key"
    assert store.get("WORK") == "secret-key"
    assert store.exists("Work")


def test_connection_names_are_trimmed():
    store = InMemoryProviderCredentialStore()

    store.set("  work  ", "secret-key")

    assert store.get("work") == "secret-key"


def test_multiple_connections_can_store_independent_credentials():
    store = InMemoryProviderCredentialStore()

    store.set("work", "work-secret")
    store.set("personal", "personal-secret")

    assert store.get("work") == "work-secret"
    assert store.get("personal") == "personal-secret"


def test_missing_credential_returns_none():
    store = InMemoryProviderCredentialStore()

    assert store.get("work") is None
    assert not store.exists("work")


def test_delete_removes_credential():
    store = InMemoryProviderCredentialStore()

    store.set("work", "secret-key")
    store.delete("work")

    assert store.get("work") is None
    assert not store.exists("work")


def test_delete_missing_credential_is_safe():
    store = InMemoryProviderCredentialStore()

    store.delete("work")

    assert not store.exists("work")


def test_list_returns_connection_names_only():
    store = InMemoryProviderCredentialStore()

    store.set("work", "work-secret")
    store.set("personal", "personal-secret")

    connections = store.list()

    assert connections == ["work", "personal"]
    assert "work-secret" not in connections
    assert "personal-secret" not in connections


def test_set_replaces_existing_connection_credential():
    store = InMemoryProviderCredentialStore()

    store.set("work", "old-secret")
    store.set("work", "new-secret")

    assert store.get("work") == "new-secret"


@pytest.mark.parametrize(
    "connection_name",
    ["", "   "],
)
def test_empty_connection_name_is_rejected(connection_name):
    store = InMemoryProviderCredentialStore()

    with pytest.raises(
        ValueError,
        match="Connection name cannot be empty",
    ):
        store.set(connection_name, "secret-key")


def test_empty_credential_is_rejected():
    store = InMemoryProviderCredentialStore()

    with pytest.raises(
        ValueError,
        match="Credential cannot be empty",
    ):
        store.set("work", "")
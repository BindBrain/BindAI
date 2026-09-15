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

    store.set("openai", "secret-key")

    assert store.get("openai") == "secret-key"


def test_provider_names_are_case_insensitive():
    store = InMemoryProviderCredentialStore()

    store.set("OpenAI", "secret-key")

    assert store.get("openai") == "secret-key"
    assert store.get("OPENAI") == "secret-key"
    assert store.exists("OpenAI")


def test_provider_names_are_trimmed():
    store = InMemoryProviderCredentialStore()

    store.set("  openai  ", "secret-key")

    assert store.get("openai") == "secret-key"


def test_missing_credential_returns_none():
    store = InMemoryProviderCredentialStore()

    assert store.get("openai") is None
    assert not store.exists("openai")


def test_delete_removes_credential():
    store = InMemoryProviderCredentialStore()

    store.set("openai", "secret-key")
    store.delete("openai")

    assert store.get("openai") is None
    assert not store.exists("openai")


def test_delete_missing_credential_is_safe():
    store = InMemoryProviderCredentialStore()

    store.delete("openai")

    assert not store.exists("openai")


def test_list_returns_provider_names_only():
    store = InMemoryProviderCredentialStore()

    store.set("openai", "openai-secret")
    store.set("anthropic", "anthropic-secret")

    providers = store.list()

    assert providers == ["openai", "anthropic"]
    assert "openai-secret" not in providers
    assert "anthropic-secret" not in providers


def test_set_replaces_existing_credential():
    store = InMemoryProviderCredentialStore()

    store.set("openai", "old-secret")
    store.set("openai", "new-secret")

    assert store.get("openai") == "new-secret"


@pytest.mark.parametrize(
    "provider",
    ["", "   "],
)
def test_empty_provider_is_rejected(provider):
    store = InMemoryProviderCredentialStore()

    with pytest.raises(ValueError, match="Provider cannot be empty"):
        store.set(provider, "secret-key")


def test_empty_credential_is_rejected():
    store = InMemoryProviderCredentialStore()

    with pytest.raises(ValueError, match="Credential cannot be empty"):
        store.set("openai", "")
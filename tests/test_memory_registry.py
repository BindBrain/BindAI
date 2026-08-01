import pytest

from bindai_memory import MemoryRegistry


def test_memory_registry_contains_defaults():

    providers = MemoryRegistry.providers()

    assert "memory" in providers
    assert "sqlite" in providers
    assert "vector" in providers


def test_unknown_memory_provider():

    with pytest.raises(ValueError):

        MemoryRegistry.provider(
            "does_not_exist",
        )
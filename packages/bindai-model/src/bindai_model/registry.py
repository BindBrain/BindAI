from __future__ import annotations

from bindai_core.model import ModelProvider


class ModelRegistry:
    """
    Registry of model providers.
    """

    def __init__(self):
        self._providers: dict[str, ModelProvider] = {}

    def register(
        self,
        provider: ModelProvider,
    ) -> None:
        self._providers[provider.name] = provider

    def get(
        self,
        name: str,
    ) -> ModelProvider:
        return self._providers[name]

    def contains(
        self,
        name: str,
    ) -> bool:
        return name in self._providers

    def names(
        self,
    ) -> list[str]:
        return sorted(self._providers.keys())

    def all(
        self,
    ) -> list[ModelProvider]:
        return list(self._providers.values())

    def remove(
        self,
        name: str,
    ) -> None:
        del self._providers[name]

    def clear(
        self,
    ) -> None:
        self._providers.clear()

    def __len__(
        self,
    ) -> int:
        return len(self._providers)
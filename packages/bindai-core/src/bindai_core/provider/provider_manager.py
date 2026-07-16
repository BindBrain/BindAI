from __future__ import annotations

from bindai_core.model import ModelProvider


class ProviderManager:
    """
    Registers and resolves ModelProvider instances.
    """

    def __init__(self):
        self._providers: dict[str, ModelProvider] = {}
        self._default: str | None = None

    def register(
        self,
        provider: ModelProvider,
        *,
        default: bool = False,
    ) -> None:

        self._providers[provider.name] = provider

        if default or self._default is None:
            self._default = provider.name

    def get(
        self,
        name: str,
    ) -> ModelProvider:

        return self._providers[name]

    def default(self) -> ModelProvider:

        if self._default is None:
            raise RuntimeError("No default provider registered.")

        return self._providers[self._default]

    def names(self) -> list[str]:
        return list(self._providers.keys())

    def __len__(self) -> int:
        return len(self._providers)
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from bindai_core import ProviderFactory


class ProviderRegistry:
    """
    Compatibility facade over the canonical BindAI core provider registry.
    """

    @classmethod
    def register(
        cls,
        name: str,
        builder: Callable,
    ) -> None:
        ProviderFactory.register(
            name,
            builder,
        )

    @classmethod
    def unregister(
        cls,
        name: str,
    ) -> None:
        ProviderFactory._providers.pop(
            name.lower(),
            None,
        )

    @classmethod
    def exists(
        cls,
        name: str,
    ) -> bool:
        return name.lower() in ProviderFactory._providers

    @classmethod
    def get(
        cls,
        name: str,
    ) -> Callable:
        try:
            return ProviderFactory._providers[
                name.lower()
            ]
        except KeyError as exc:
            raise ValueError(
                f"Unknown provider '{name}'."
            ) from exc

    @classmethod
    def create(
        cls,
        name: str,
        configuration=None,
        **kwargs: Any,
    ):
        if kwargs:
            return cls.get(name)(
                **kwargs,
            )

        return ProviderFactory.create(
            name,
            configuration,
        )

    @classmethod
    def list(
        cls,
    ) -> list[str]:
        return list(
            ProviderFactory.names(),
        )

    @classmethod
    def clear(
        cls,
    ) -> None:
        ProviderFactory._providers.clear()
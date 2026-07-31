from __future__ import annotations

from collections.abc import Callable


class ProviderRegistry:
    """
    Registry for provider implementations.
    """

    _providers: dict[str, Callable] = {}

    @classmethod
    def register(
        cls,
        name: str,
        builder: Callable,
    ) -> None:
        cls._providers[name] = builder

    @classmethod
    def unregister(
        cls,
        name: str,
    ) -> None:
        cls._providers.pop(name, None)

    @classmethod
    def exists(
        cls,
        name: str,
    ) -> bool:
        return name in cls._providers

    @classmethod
    def get(
        cls,
        name: str,
    ) -> Callable:
        try:
            return cls._providers[name]

        except KeyError as exc:
            raise ValueError(f"Unknown provider '{name}'.") from exc

    @classmethod
    def create(
        cls,
        name: str,
        **kwargs,
    ):
        builder = cls.get(name)

        return builder(**kwargs)

    @classmethod
    def list(
        cls,
    ) -> list[str]:
        return sorted(cls._providers.keys())

    @classmethod
    def clear(
        cls,
    ) -> None:
        cls._providers.clear()

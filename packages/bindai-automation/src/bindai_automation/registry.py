from __future__ import annotations

from bindai_core.registry import Registry

from .trigger import Trigger


class TriggerRegistry:
    """
    Registry for automation triggers.
    """

    def __init__(self) -> None:
        self._registry = Registry()

    def register(
        self,
        key: str,
        trigger: Trigger,
    ) -> None:
        self._registry.register(
            key,
            trigger,
        )

    def get(
        self,
        key: str,
    ) -> Trigger:
        return self._registry.get(
            key,
        )

    def get_or_none(
        self,
        key: str,
    ) -> Trigger | None:
        return self._registry.get_or_none(
            key,
        )

    def remove(
        self,
        key: str,
    ) -> None:
        self._registry.remove(
            key,
        )

    def contains(
        self,
        key: str,
    ) -> bool:
        return self._registry.contains(
            key,
        )

    def clear(self) -> None:
        self._registry.clear()

    def keys(self) -> tuple[str, ...]:
        return self._registry.keys()

    def values(self) -> tuple[Trigger, ...]:
        return self._registry.values()

    def items(self) -> tuple[str, Trigger]:
        return self._registry.items()

    def __len__(self) -> int:
        return len(self._registry)
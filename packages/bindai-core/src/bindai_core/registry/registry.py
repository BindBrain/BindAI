from __future__ import annotations

from typing import Any


class Registry:
    """
    Generic registry used across BindAI.

    Stores named objects such as providers,
    workflows, tools, agents, triggers, etc.
    """

    def __init__(self) -> None:
        self._items: dict[str, Any] = {}

    def register(self, key: str, value: Any) -> None:
        if key in self._items:
            raise ValueError(
                f"'{key}' is already registered."
            )

        self._items[key] = value

    def get(self, key: str) -> Any:
        if key not in self._items:
            raise KeyError(
                f"'{key}' is not registered."
            )

        return self._items[key]

    def remove(self, key: str) -> None:
        self._items.pop(key, None)

    def contains(self, key: str) -> bool:
        return key in self._items

    def clear(self) -> None:
        self._items.clear()

    def keys(self):
        return tuple(self._items.keys())

    def values(self):
        return tuple(self._items.values())

    def items(self):
        return tuple(self._items.items())

    def __len__(self) -> int:
        return len(self._items)
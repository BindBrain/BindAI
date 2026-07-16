from __future__ import annotations


class Manager:
    """
    Base manager used by BindAI subsystems.
    """

    def __init__(self):
        self._items: dict[str, object] = {}

    def add(self, name: str, item: object):
        self._items[name] = item
        return self

    def get(self, name: str):
        return self._items[name]

    def exists(self, name: str) -> bool:
        return name in self._items

    def remove(self, name: str):
        self._items.pop(name, None)

    def all(self):
        return list(self._items.values())

    def names(self):
        return list(self._items.keys())

    def clear(self):
        self._items.clear()

    def __len__(self):
        return len(self._items)
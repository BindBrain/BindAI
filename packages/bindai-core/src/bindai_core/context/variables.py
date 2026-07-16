from __future__ import annotations


class Variables:
    """
    Stores execution variables.
    """

    def __init__(self):
        self._values: dict[str, object] = {}

    def set(self, key: str, value: object) -> None:
        self._values[key] = value

    def get(self, key: str, default=None):
        return self._values.get(key, default)

    def contains(self, key: str) -> bool:
        return key in self._values

    def remove(self, key: str) -> None:
        self._values.pop(key, None)

    def clear(self) -> None:
        self._values.clear()

    def as_dict(self) -> dict[str, object]:
        return dict(self._values)
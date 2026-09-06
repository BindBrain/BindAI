from __future__ import annotations

from .connection import Connection


class ConnectionRegistry:
    """Registry for named BindAI connection types."""

    _connections: dict[str, type[Connection]] = {}

    @classmethod
    def register(cls, name: str, connection_type: type[Connection]) -> None:
        if not name.strip():
            raise ValueError("Connection name cannot be empty.")
        cls._connections[name] = connection_type

    @classmethod
    def provider(cls, name: str) -> type[Connection]:
        try:
            return cls._connections[name]
        except KeyError:
            raise KeyError(f"Connection '{name}' is not registered.") from None

    @classmethod
    def names(cls) -> tuple[str, ...]:
        return tuple(sorted(cls._connections))

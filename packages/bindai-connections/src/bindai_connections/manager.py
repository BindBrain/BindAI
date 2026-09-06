from __future__ import annotations

from .connection import Connection


class ConnectionManager:
    """Manage active BindAI connections."""

    def __init__(self) -> None:
        self._connections: dict[str, Connection] = {}

    def add(self, connection: Connection) -> ConnectionManager:
        self._connections[connection.name] = connection
        return self

    def get(self, name: str) -> Connection:
        try:
            return self._connections[name]
        except KeyError:
            raise KeyError(f"Connection '{name}' is not managed.") from None

    def contains(self, name: str) -> bool:
        return name in self._connections

    def remove(self, name: str) -> None:
        connection = self._connections.pop(name, None)
        if connection is not None and connection.is_connected():
            connection.disconnect()

    def connect(self, name: str) -> Connection:
        connection = self.get(name)
        connection.connect()
        return connection

    def disconnect(self, name: str) -> Connection:
        connection = self.get(name)
        connection.disconnect()
        return connection

    def disconnect_all(self) -> None:
        for connection in self._connections.values():
            if connection.is_connected():
                connection.disconnect()

    def all(self) -> list[Connection]:
        return list(self._connections.values())

    def names(self) -> list[str]:
        return list(self._connections.keys())

    def clear(self) -> None:
        self.disconnect_all()
        self._connections.clear()

    def size(self) -> int:
        return len(self._connections)
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ConnectionMetadata:
    """Non-secret metadata describing a configured provider connection."""

    name: str
    provider: str


class ConnectionManifest:
    """Persist non-secret provider connection metadata for a project."""

    DEFAULT_PATH = Path(".bindai") / "connections.toml"

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or self.DEFAULT_PATH

    @property
    def path(self) -> Path:
        return self._path

    def add(self, name: str, provider: str) -> None:
        connection = self._normalize(name, provider)
        connections = [
            existing
            for existing in self._load()
            if existing.name != connection.name
        ]
        connections.append(connection)
        self._write(connections)

    def get(self, name: str) -> ConnectionMetadata | None:
        connection_name = self._normalize_name(name)

        for connection in self._load():
            if connection.name == connection_name:
                return connection

        return None

    def remove(self, name: str) -> None:
        connection_name = self._normalize_name(name)
        connections = [
            connection
            for connection in self._load()
            if connection.name != connection_name
        ]
        self._write(connections)

    def list(self) -> list[ConnectionMetadata]:
        return self._load()

    def _load(self) -> list[ConnectionMetadata]:
        if not self._path.exists():
            return []

        with self._path.open("rb") as file:
            data = tomllib.load(file)

        raw_connections = data.get("connections", [])

        if not isinstance(raw_connections, list):
            raise ValueError("Connection manifest must contain an array.")

        connections: list[ConnectionMetadata] = []

        for raw in raw_connections:
            if not isinstance(raw, dict):
                raise ValueError(
                    "Each connection manifest entry must be a table.",
                )

            name = raw.get("name")
            provider = raw.get("provider")

            if not isinstance(name, str) or not isinstance(provider, str):
                raise ValueError(
                    "Connection manifest entries require name and provider.",
                )

            connections.append(self._normalize(name, provider))

        return connections

    def _write(self, connections: list[ConnectionMetadata]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)

        chunks: list[str] = []

        for connection in connections:
            chunks.extend(
                [
                    "[[connections]]",
                    f'name = "{connection.name}"',
                    f'provider = "{connection.provider}"',
                    "",
                ],
            )

        self._path.write_text(
            "\n".join(chunks),
            encoding="utf-8",
        )

    @classmethod
    def _normalize(
        cls,
        name: str,
        provider: str,
    ) -> ConnectionMetadata:
        return ConnectionMetadata(
            name=cls._normalize_name(name),
            provider=cls._normalize_provider(provider),
        )

    @staticmethod
    def _normalize_name(name: str) -> str:
        normalized = name.strip().lower()

        if not normalized:
            raise ValueError("Connection name cannot be empty.")

        return normalized

    @staticmethod
    def _normalize_provider(provider: str) -> str:
        normalized = provider.strip().lower()

        if not normalized:
            raise ValueError("Provider cannot be empty.")

        return normalized
from __future__ import annotations

import os
from dataclasses import dataclass, fields
from typing import Any, get_type_hints


@dataclass(frozen=True, slots=True)
class ConfigValue:
    value: Any
    source: str


class ConfigResolver:
    """Resolve configuration values and report where each value came from."""

    _ENV_PREFIX = "BINDAI_"

    def __init__(
        self,
        config: Any,
        configured_fields: set[str] | frozenset[str] | None = None,
        environ: dict[str, str] | None = None,
    ) -> None:
        self.config = config
        self.configured_fields = (
            frozenset(configured_fields)
            if configured_fields is not None
            else frozenset()
        )
        self.environ = os.environ if environ is None else environ

    def resolve(self, name: str) -> ConfigValue:
        """Resolve one field using environment, TOML, then defaults."""
        config_fields = {field.name: field for field in fields(self.config)}

        if name not in config_fields:
            raise KeyError(f'Unknown configuration field "{name}".')

        environment_name = self._environment_name(name)

        if environment_name in self.environ:
            field_types = get_type_hints(type(self.config))

            return ConfigValue(
                value=self._convert(
                    field_types[name],
                    self.environ[environment_name],
                ),
                source=f"environment:{environment_name}",
            )

        if name in self.configured_fields:
            return ConfigValue(
                value=getattr(self.config, name),
                source="bindai.toml",
            )

        return ConfigValue(
            value=getattr(self.config, name),
            source="default",
        )

    def all(self) -> dict[str, ConfigValue]:
        """Resolve every configuration field."""
        return {
            field.name: self.resolve(field.name)
            for field in fields(self.config)
        }

    def _environment_name(self, name: str) -> str:
        return f"{self._ENV_PREFIX}{name.upper()}"

    def _convert(self, field_type: Any, value: str) -> Any:
        if field_type is str:
            return value

        if field_type is int:
            return int(value)

        if field_type is float:
            return float(value)

        if field_type is bool:
            normalized = value.strip().lower()

            if normalized in {"1", "true", "yes", "on"}:
                return True

            if normalized in {"0", "false", "no", "off"}:
                return False

            raise ValueError(f'Invalid boolean value "{value}".')

        return value
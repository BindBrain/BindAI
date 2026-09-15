from __future__ import annotations

import os
import re
import tempfile
import tomllib
from dataclasses import fields
from pathlib import Path
from typing import Any, get_args, get_type_hints

from .project import ProjectConfig


class TomlWriter:
    """Perform targeted writes to a flat ProjectConfig TOML file."""

    _KEY_PATTERN = re.compile(
        r"^(?P<prefix>\s*)(?P<key>[A-Za-z0-9_-]+)"
        r"(?P<separator>\s*=\s*)(?P<value>.*)$"
    )

    def set(
        self,
        path: str | Path,
        name: str,
        value: Any,
    ) -> None:
        """Set one top-level ProjectConfig field."""
        path = Path(path)

        expected_type = self._field_type(name)
        self._validate_value(name, value, expected_type)

        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            self._atomic_write(
                path,
                f"{name} = {self._serialize(value)}\n",
            )
            return

        content = path.read_text(encoding="utf-8")

        self._validate_document(content)

        lines = content.splitlines(keepends=True)
        replacement = self._serialize(value)
        updated = False

        for index, line in enumerate(lines):
            match = self._KEY_PATTERN.match(line)

            if match is None or match.group("key") != name:
                continue

            if line.endswith("\r\n"):
                line_ending = "\r\n"
            elif line.endswith("\n"):
                line_ending = "\n"
            else:
                line_ending = ""

            value_text = match.group("value")
            inline_comment = self._inline_comment(value_text)

            lines[index] = (
                f"{match.group('prefix')}"
                f"{name}"
                f"{match.group('separator')}"
                f"{replacement}"
                f"{inline_comment}"
                f"{line_ending}"
            )
            updated = True
            break

        if not updated:
            if content and not content.endswith(("\n", "\r")):
                content += "\n"

            content += f"{name} = {replacement}\n"
        else:
            content = "".join(lines)

        self._atomic_write(path, content)

    def _field_type(self, name: str) -> Any:
        config_fields = {
            field.name: field
            for field in fields(ProjectConfig)
        }

        if name not in config_fields:
            raise KeyError(
                f'Unknown configuration field "{name}".'
            )

        return get_type_hints(ProjectConfig)[name]

    def _validate_value(
        self,
        name: str,
        value: Any,
        expected_type: Any,
    ) -> None:
        expected_types = get_args(expected_type)

        if expected_types:
            if type(value) not in expected_types:
                type_names = ", ".join(
                    expected_type.__name__
                    for expected_type in expected_types
                    if hasattr(expected_type, "__name__")
                )

                raise TypeError(
                    f'Invalid value for configuration field "{name}": '
                    f"expected {type_names}, "
                    f"got {type(value).__name__}.",
                )

            return

        if type(value) is not expected_type:
            raise TypeError(
                f'Invalid value for configuration field "{name}": '
                f"expected {expected_type.__name__}, "
                f"got {type(value).__name__}.",
            )

    def _validate_document(self, content: str) -> None:
        try:
            data = tomllib.loads(content)
        except tomllib.TOMLDecodeError as exc:
            raise ValueError(
                "bindai.toml contains invalid TOML.",
            ) from exc

        if any(
            isinstance(value, dict)
            for value in data.values()
        ):
            raise ValueError(
                "TomlWriter only supports top-level "
                "configuration fields.",
            )

    def _inline_comment(self, value: str) -> str:
        in_string = False
        escaped = False

        for index, character in enumerate(value):
            if escaped:
                escaped = False
                continue

            if character == "\\" and in_string:
                escaped = True
                continue

            if character == '"':
                in_string = not in_string
                continue

            if character == "#" and not in_string:
                return value[index - 1 :]

        return ""

    def _serialize(self, value: Any) -> str:
        if isinstance(value, str):
            escaped = (
                value.replace("\\", "\\\\")
                .replace('"', '\\"')
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t")
            )
            return f'"{escaped}"'

        if isinstance(value, bool):
            return "true" if value else "false"

        if isinstance(value, (int, float)):
            return str(value)

        raise TypeError(
            f"Unsupported TOML value type: {type(value).__name__}.",
        )

    def _atomic_write(
        self,
        path: Path,
        content: str,
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

        fd, temporary_path = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            text=True,
        )

        try:
            with os.fdopen(
                fd,
                "w",
                encoding="utf-8",
                newline="",
            ) as temporary_file:
                temporary_file.write(content)
                temporary_file.flush()
                os.fsync(temporary_file.fileno())

            os.replace(temporary_path, path)
        except Exception:
            try:
                os.unlink(temporary_path)
            except FileNotFoundError:
                pass
            raise
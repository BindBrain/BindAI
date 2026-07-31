from __future__ import annotations

import tomllib
from pathlib import Path

from .project import ProjectConfig


class TomlLoader:
    def load(
        self,
        path: str | Path,
    ) -> ProjectConfig:

        with open(
            path,
            "rb",
        ) as f:
            data = tomllib.load(f)

        return ProjectConfig(
            **data,
        )

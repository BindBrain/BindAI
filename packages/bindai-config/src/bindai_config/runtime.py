from __future__ import annotations

from pathlib import Path

from .project import ProjectConfig
from .toml_loader import TomlLoader


class ProjectRuntime:
    def __init__(
        self,
        root: Path,
    ):
        self.root = root

        self.config = self._load()

    def _load(
        self,
    ) -> ProjectConfig:

        config = self.root / "bindai.toml"

        if not config.exists():
            return ProjectConfig()

        return TomlLoader().load(
            config,
        )

    @property
    def project(self):
        return self.config.project

    @property
    def default(self):
        return self.config.default

    @property
    def paths(self):
        return self.config.paths

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
    def project(self) -> ProjectConfig:
        return self.config

    @property
    def default(self) -> ProjectConfig:
        return self.config

    @property
    def paths(self) -> dict[str, str]:
        return {
            "memory": self.config.memory,
            "knowledge": self.config.knowledge,
            "templates": self.config.templates,
            "workflows": self.config.workflows,
            "agents": self.config.agents,
            "tools": self.config.tools,
        }

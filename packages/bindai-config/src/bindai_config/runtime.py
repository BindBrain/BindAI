from __future__ import annotations

from pathlib import Path

from .project import ProjectConfig
from .resolver import ConfigResolver
from .toml_loader import TomlLoader


class ProjectRuntime:
    def __init__(
        self,
        root: Path,
    ):
        self.root = root
        self.config, self.configured_fields = self._load()

    def _load(
        self,
    ) -> tuple[ProjectConfig, frozenset[str]]:

        config = self.root / "bindai.toml"

        if not config.exists():
            return ProjectConfig(), frozenset()

        return TomlLoader().load_with_fields(
            config,
        )

    @property
    def project(self) -> ProjectConfig:
        return self.config

    @property
    def default(self) -> ProjectConfig:
        return self.config

    @property
    def resolver(self) -> ConfigResolver:
        return ConfigResolver(
            self.config,
            configured_fields=self.configured_fields,
        )

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
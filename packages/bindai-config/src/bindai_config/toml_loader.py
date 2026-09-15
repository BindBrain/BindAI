from __future__ import annotations

import tomllib
from pathlib import Path

from .application import ApplicationAgentConfig, ApplicationConfig, ModelConfig
from .project import ProjectConfig


class TomlLoader:
    def load(self, path: str | Path) -> ProjectConfig:
        with open(path, "rb") as f:
            data = tomllib.load(f)

        return ProjectConfig(**data)

    def load_application(self, path: str | Path) -> ApplicationConfig:
        with open(path, "rb") as f:
            data = tomllib.load(f)

        project = data.get("project", {})
        agent = data.get("agent")

        model = None

        if agent is not None:
            model_data = agent.get("model")

            if model_data is not None:
                model = ModelConfig(**model_data)

            agent_config = ApplicationAgentConfig(
                name=agent["name"],
                instructions=agent.get("instructions", ""),
                model=model,
            )
        else:
            agent_config = None

        return ApplicationConfig(
            name=project["name"],
            description=project.get("description", ""),
            type=project.get("type", "assistant"),
            agent=agent_config,
        )
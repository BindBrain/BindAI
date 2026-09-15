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

        project = data.get("project")

        if project is None:
            raise ValueError(
                'Missing required "project" section.'
            )

        if "name" not in project:
            raise ValueError(
                'Missing required "project.name".'
            )

        agent = data.get("agent")

        if agent is None:
            agent_config = None
        else:
            if "name" not in agent:
                raise ValueError(
                    'Missing required "agent.name".'
                )

            model_data = agent.get("model")

            if model_data is None:
                model = None
            else:
                model = ModelConfig(**model_data)

            agent_config = ApplicationAgentConfig(
                name=agent["name"],
                instructions=agent.get("instructions", ""),
                model=model,
            )

        return ApplicationConfig(
            name=project["name"],
            description=project.get("description", ""),
            type=project.get("type", "assistant"),
            agent=agent_config,
        )
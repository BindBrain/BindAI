from __future__ import annotations

from pathlib import Path

import pytest
from bindai_config import ProjectConfig, ProjectRuntime, TomlLoader


def test_project_config_defaults() -> None:
    config = ProjectConfig()

    assert config.name == "BindAI Project"
    assert config.provider == "openai"
    assert config.model == "gpt-4.1-mini"
    assert config.temperature == 0.7
    assert config.timeout == 60
    assert config.entrypoint == "main.py"
    assert config.memory == "memory"
    assert config.knowledge == "knowledge"
    assert config.templates == "templates"
    assert config.workflows == "workflows"
    assert config.agents == "agents"
    assert config.tools == "tools"


def test_project_config_accepts_custom_values() -> None:
    config = ProjectConfig(
        name="Custom Project",
        provider="anthropic",
        model="claude-sonnet",
        temperature=0.2,
        timeout=120,
        entrypoint="app.py",
        memory=".memory",
        knowledge=".knowledge",
        templates=".templates",
        workflows=".workflows",
        agents=".agents",
        tools=".tools",
    )

    assert config.name == "Custom Project"
    assert config.provider == "anthropic"
    assert config.model == "claude-sonnet"
    assert config.temperature == 0.2
    assert config.timeout == 120
    assert config.entrypoint == "app.py"
    assert config.memory == ".memory"
    assert config.knowledge == ".knowledge"
    assert config.templates == ".templates"
    assert config.workflows == ".workflows"
    assert config.agents == ".agents"
    assert config.tools == ".tools"


def test_project_runtime_uses_defaults_without_config(tmp_path: Path) -> None:
    runtime = ProjectRuntime(tmp_path)

    assert runtime.project == ProjectConfig()
    assert runtime.default == ProjectConfig()


def test_project_runtime_paths(tmp_path: Path) -> None:
    runtime = ProjectRuntime(tmp_path)

    assert runtime.paths == {
        "memory": "memory",
        "knowledge": "knowledge",
        "templates": "templates",
        "workflows": "workflows",
        "agents": "agents",
        "tools": "tools",
    }


def test_toml_loader_loads_project_config(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
name = "Example Project"
provider = "openai"
model = "gpt-4.1"
temperature = 0.4
timeout = 90
entrypoint = "app.py"
memory = ".memory"
knowledge = ".knowledge"
templates = ".templates"
workflows = ".workflows"
agents = ".agents"
tools = "tools"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    config = TomlLoader().load(config_path)

    assert config == ProjectConfig(
        name="Example Project",
        provider="openai",
        model="gpt-4.1",
        temperature=0.4,
        timeout=90,
        entrypoint="app.py",
        memory=".memory",
        knowledge=".knowledge",
        templates=".templates",
        workflows=".workflows",
        agents=".agents",
        tools="tools",
    )


def test_toml_loader_loads_application_config(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
[project]
name = "customer-support"
description = "Customer support assistant"
type = "assistant"

[agent]
name = "Support Agent"
instructions = "Help customers."

[agent.model]
provider = "openai"
model = "gpt-5"
temperature = 0.2
""".strip()
        + "\n",
        encoding="utf-8",
    )

    config = TomlLoader().load_application(config_path)

    assert config.name == "customer-support"
    assert config.description == "Customer support assistant"
    assert config.type == "assistant"

    assert config.agent is not None
    assert config.agent.name == "Support Agent"
    assert config.agent.instructions == "Help customers."

    assert config.agent.model is not None
    assert config.agent.model.provider == "openai"
    assert config.agent.model.model == "gpt-5"
    assert config.agent.model.temperature == 0.2
    assert config.agent.model.max_tokens is None


def test_toml_loader_loads_application_defaults(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
[project]
name = "minimal-app"

[agent]
name = "Assistant"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    config = TomlLoader().load_application(config_path)

    assert config.name == "minimal-app"
    assert config.description == ""
    assert config.type == "assistant"

    assert config.agent is not None
    assert config.agent.name == "Assistant"
    assert config.agent.instructions == ""
    assert config.agent.model is None


def test_toml_loader_loads_application_without_agent(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
[project]
name = "data-service"
description = "A data service"
type = "application"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    config = TomlLoader().load_application(config_path)

    assert config.name == "data-service"
    assert config.description == "A data service"
    assert config.type == "application"
    assert config.agent is None


def test_toml_loader_rejects_missing_project(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
[agent]
name = "Assistant"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match='Missing required "project" section',
    ):
        TomlLoader().load_application(config_path)


def test_toml_loader_rejects_missing_project_name(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
[project]
description = "Missing project name"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match='Missing required "project.name"',
    ):
        TomlLoader().load_application(config_path)


def test_toml_loader_rejects_missing_agent_name(tmp_path: Path) -> None:
    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
[project]
name = "customer-support"

[agent]
instructions = "Help customers."
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match='Missing required "agent.name"',
    ):
        TomlLoader().load_application(config_path)
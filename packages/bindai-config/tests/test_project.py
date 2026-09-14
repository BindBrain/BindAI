from __future__ import annotations

from pathlib import Path

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
tools = ".tools"
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
        tools=".tools",
    )
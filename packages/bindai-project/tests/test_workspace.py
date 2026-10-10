from __future__ import annotations

from pathlib import Path

import pytest

from bindai_project import ProjectWorkspace


def write_project(root: Path, *, name: str = "Test Project") -> Path:
    root.mkdir(parents=True, exist_ok=True)

    (root / "bindai.toml").write_text(
        f'''name = "{name}"
provider = "openai"
model = "gpt-4.1-mini"
workflows = "workflows"
''',
        encoding="utf-8",
    )

    return root


def test_workspace_discovers_projects(tmp_path: Path):
    first = write_project(tmp_path / "first", name="First")
    second = write_project(tmp_path / "second", name="Second")
    (tmp_path / "not-a-project").mkdir()

    workspace = ProjectWorkspace(tmp_path)

    projects = workspace.discover()

    assert [project.root for project in projects] == [
        first.resolve(),
        second.resolve(),
    ]


def test_workspace_can_open_project(tmp_path: Path):
    project = write_project(tmp_path / "demo", name="Demo")

    workspace = ProjectWorkspace(tmp_path)

    repository = workspace.open_project("demo")

    assert repository.root == project.resolve()
    assert repository.config.name == "Demo"


def test_workspace_project_root_opens_itself(tmp_path: Path):
    project = write_project(tmp_path / "demo")

    workspace = ProjectWorkspace(project)

    projects = workspace.discover()

    assert len(projects) == 1
    assert projects[0].root == project.resolve()


def test_workspace_rejects_non_project(tmp_path: Path):
    (tmp_path / "not-a-project").mkdir()

    workspace = ProjectWorkspace(tmp_path)

    with pytest.raises(ValueError, match="Not a BindAI project"):
        workspace.open_project("not-a-project")

def test_create_project(tmp_path):
    workspace = ProjectWorkspace(tmp_path)

    repository = workspace.create_project("created-project")

    assert repository.root == (tmp_path / "created-project").resolve()
    assert repository.is_project()
    assert repository.config.name == "created-project"
    assert (repository.root / ".env").is_file()

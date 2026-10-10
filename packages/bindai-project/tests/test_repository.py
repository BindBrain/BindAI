from __future__ import annotations

from pathlib import Path

import pytest

from bindai_project import ProjectRepository


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


def write_workflow(root: Path, workflow_id: str = "demo") -> Path:
    workflows = root / "workflows"
    workflows.mkdir(parents=True, exist_ok=True)

    path = workflows / f"{workflow_id}.yaml"

    path.write_text(
        f'''version: 1
workflow:
  id: {workflow_id}
  name: Demo Workflow
  nodes:
    - id: start
      type: start
    - id: end
      type: end
  edges:
    - from: start
      to: end
''',
        encoding="utf-8",
    )

    return path


def test_project_detection(tmp_path: Path):
    project = write_project(tmp_path / "project")

    repository = ProjectRepository(project)

    assert repository.is_project() is True
    assert repository.root == project.resolve()
    assert repository.config.name == "Test Project"


def test_non_project_directory(tmp_path: Path):
    repository = ProjectRepository(tmp_path)

    assert repository.is_project() is False


def test_workflow_directory_uses_project_configuration(tmp_path: Path):
    project = write_project(tmp_path / "project")

    repository = ProjectRepository(project)

    assert repository.workflow_directory() == project.resolve() / "workflows"


def test_workflow_paths_discovers_supported_files(tmp_path: Path):
    project = write_project(tmp_path / "project")

    yaml_path = write_workflow(project, "first")

    workflows = project / "workflows"
    (workflows / "notes.txt").write_text("ignore", encoding="utf-8")
    nested = workflows / "nested"
    nested.mkdir()
    (nested / "second.yml").write_text(
        "version: 1\nworkflow:\n  id: second\n  name: Second\n  nodes: []\n  edges: []\n",
        encoding="utf-8",
    )

    repository = ProjectRepository(project)

    paths = repository.workflow_paths()

    assert paths == sorted(
        [
            yaml_path.resolve(),
            (nested / "second.yml").resolve(),
        ]
    )


def test_load_workflow(tmp_path: Path):
    project = write_project(tmp_path / "project")
    workflow_path = write_workflow(project, "demo")

    repository = ProjectRepository(project)

    workflow = repository.load_workflow(workflow_path)

    assert workflow.id == "demo"
    assert workflow.name == "Demo Workflow"
    assert [node.id for node in workflow.nodes] == ["start", "end"]
    assert workflow.edges[0].source == "start"
    assert workflow.edges[0].target == "end"


def test_save_workflow_roundtrip(tmp_path: Path):
    project = write_project(tmp_path / "project")
    source = write_workflow(project, "demo")

    repository = ProjectRepository(project)

    workflow = repository.load_workflow(source)

    saved = repository.save_workflow(workflow, "workflows/copied.yaml")

    assert saved == (project / "workflows" / "copied.yaml").resolve()
    assert saved.is_file()

    loaded = repository.load_workflow(saved)

    assert loaded.to_dict() == workflow.to_dict()


def test_save_workflow_uses_default_path(tmp_path: Path):
    project = write_project(tmp_path / "project")
    source = write_workflow(project, "demo")

    repository = ProjectRepository(project)

    workflow = repository.load_workflow(source)
    saved = repository.save_workflow(workflow)

    assert saved == (project / "workflows" / "demo.yaml").resolve()


def test_discover_projects(tmp_path: Path):
    first = write_project(tmp_path / "first", name="First")
    second = write_project(tmp_path / "second", name="Second")

    (tmp_path / "not-a-project").mkdir()

    repositories = ProjectRepository.discover(tmp_path)

    assert [repository.root for repository in repositories] == [
        first.resolve(),
        second.resolve(),
    ]


def test_project_paths_cannot_escape_root(tmp_path: Path):
    project = write_project(tmp_path / "project")
    repository = ProjectRepository(project)

    with pytest.raises(ValueError, match="inside project directory"):
        repository.load_workflow(tmp_path / "outside.yaml")


def test_copy_project_is_portable(tmp_path: Path):
    project = write_project(tmp_path / "project")
    write_workflow(project, "portable")

    repository = ProjectRepository(project)

    copied = repository.copy_to(tmp_path / "copied")

    assert copied.root == (tmp_path / "copied").resolve()
    assert copied.is_project() is True

    workflows = copied.workflow_paths()

    assert workflows == [
        (tmp_path / "copied" / "workflows" / "portable.yaml").resolve()
    ]

    loaded = copied.load_workflow(workflows[0])

    assert loaded.id == "portable"
    assert loaded.name == "Demo Workflow"

from pathlib import Path

import pytest

from bindai_project import ProjectCreator


def test_create_project_from_scaffold(tmp_path: Path) -> None:
    scaffold = tmp_path / "scaffold"
    scaffold.mkdir()

    (scaffold / "bindai.toml").write_text(
        'name = "{{ project_name }}"\n',
        encoding="utf-8",
    )
    (scaffold / ".env.example").write_text(
        "BINDAI_API_KEY=\n",
        encoding="utf-8",
    )
    (scaffold / "README.md").write_text(
        "# {{PROJECT_NAME}}\n",
        encoding="utf-8",
    )
    (scaffold / "workflows").mkdir()
    (scaffold / "workflows" / ".gitkeep").write_text(
        "",
        encoding="utf-8",
    )

    destination = tmp_path / "my-project"

    repository = ProjectCreator(scaffold).create(destination)

    assert repository.root == destination.resolve()
    assert repository.is_project()
    assert repository.config.name == "my-project"
    assert (destination / ".env").is_file()
    assert (destination / "workflows").is_dir()

    assert (destination / "README.md").read_text(
        encoding="utf-8",
    ) == "# my-project\n"


def test_create_project_uses_explicit_project_name(
    tmp_path: Path,
) -> None:
    scaffold = tmp_path / "scaffold"
    scaffold.mkdir()

    (scaffold / "bindai.toml").write_text(
        'name = "{{ project_name }}"\n',
        encoding="utf-8",
    )

    destination = tmp_path / "project-directory"

    repository = ProjectCreator(scaffold).create(
        destination,
        project_name="My Application",
    )

    assert repository.config.name == "My Application"


def test_create_project_rejects_existing_destination(
    tmp_path: Path,
) -> None:
    scaffold = tmp_path / "scaffold"
    scaffold.mkdir()

    destination = tmp_path / "existing"
    destination.mkdir()

    with pytest.raises(FileExistsError):
        ProjectCreator(scaffold).create(destination)


def test_create_project_rejects_missing_scaffold(
    tmp_path: Path,
) -> None:
    scaffold = tmp_path / "missing"
    destination = tmp_path / "project"

    with pytest.raises(ValueError):
        ProjectCreator(scaffold).create(destination)

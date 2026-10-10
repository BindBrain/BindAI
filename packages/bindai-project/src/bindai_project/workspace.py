from __future__ import annotations

from pathlib import Path

from .repository import ProjectRepository
from .creator import ProjectCreator

class ProjectWorkspace:
    """Filesystem-backed workspace for discovering and opening BindAI projects."""

    def __init__(self, root: str | Path):
        self.root = Path(root).expanduser().resolve()

    def is_project(self) -> bool:
        return (self.root / "bindai.toml").is_file()

    def discover(self) -> list[ProjectRepository]:
        if self.is_project():
            return [ProjectRepository(self.root)]

        return ProjectRepository.discover(self.root)

    def open_project(self, path: str | Path) -> ProjectRepository:
        candidate = Path(path).expanduser()

        if not candidate.is_absolute():
            candidate = self.root / candidate

        repository = ProjectRepository(candidate)

        if not repository.is_project():
            raise ValueError(
                f"Not a BindAI project: {repository.root}"
            )

        return repository

    def create_project(
        self,
        name: str,
    ) -> ProjectRepository:
        destination = self.root / name

        creator = ProjectCreator()
        return creator.create(
            destination,
            project_name=name,
        )

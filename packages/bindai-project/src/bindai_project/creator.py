from __future__ import annotations

import shutil
from pathlib import Path

from .repository import ProjectRepository


class ProjectCreator:
    """Creates portable BindAI projects from a filesystem scaffold."""

    def __init__(self, scaffold: str | Path | None = None):
        if scaffold is None:
            scaffold = Path(__file__).parent / "scaffolds" / "basic"

        self.scaffold = Path(scaffold).expanduser().resolve()

    def create(
        self,
        destination: str | Path,
        *,
        project_name: str | None = None,
    ) -> ProjectRepository:
        destination_path = Path(destination).expanduser().resolve()

        if not self.scaffold.is_dir():
            raise ValueError(
                f"Project scaffold directory does not exist: {self.scaffold}"
            )

        if destination_path.exists():
            raise FileExistsError(
                f"Project destination already exists: {destination_path}"
            )

        name = project_name or destination_path.name

        shutil.copytree(
            self.scaffold,
            destination_path,
        )

        self._replace_placeholders(
            destination_path,
            name,
        )

        example = destination_path / ".env.example"
        env = destination_path / ".env"

        if example.exists() and not env.exists():
            shutil.copy2(
                example,
                env,
            )

        return ProjectRepository(destination_path)

    @staticmethod
    def _replace_placeholders(
        root: Path,
        project_name: str,
    ) -> None:
        for file in root.rglob("*"):
            if not file.is_file():
                continue

            if file.suffix not in {
                ".py",
                ".toml",
                ".md",
                ".txt",
                ".example",
            }:
                continue

            text = file.read_text(
                encoding="utf-8",
            )

            text = text.replace(
                "{{ project_name }}",
                project_name,
            )

            text = text.replace(
                "{{PROJECT_NAME}}",
                project_name,
            )

            file.write_text(
                text,
                encoding="utf-8",
            )

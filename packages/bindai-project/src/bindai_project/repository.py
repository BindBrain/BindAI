from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from shutil import copytree

from bindai_agent import AgentDefinition, AgentDefinitionLoader
from bindai_config import ProjectRuntime
from bindai_workflow import (
    WorkflowDefinition,
    WorkflowDefinitionLoader,
)

from .forms import FormDefinition


@dataclass(frozen=True, slots=True)
class AgentSummary:
    id: str
    name: str
    path: Path


@dataclass(frozen=True, slots=True)
class FormSummary:
    id: str
    name: str
    path: Path


class ProjectRepository:
    """
    Filesystem-backed repository for a BindAI project.

    The project directory is the source of truth. This repository is
    responsible for discovering project files and loading/saving their
    portable definitions. It does not replace the existing runtime Project.
    """

    def __init__(self, path: str | Path):
        self.root = Path(path).expanduser().resolve()
        self.runtime = ProjectRuntime(self.root)

    @property
    def config(self):
        return self.runtime.project

    def is_project(self) -> bool:
        return (self.root / "bindai.toml").is_file()

    @classmethod
    def discover(cls, parent: str | Path) -> list["ProjectRepository"]:
        parent_path = Path(parent).expanduser().resolve()

        if not parent_path.is_dir():
            return []

        projects: list[ProjectRepository] = []

        for child in sorted(parent_path.iterdir()):
            if not child.is_dir():
                continue

            if not (child / "bindai.toml").is_file():
                continue

            repository = cls(child)
            projects.append(repository)

        return projects

    def workflow_directory(self) -> Path:
        return self.root / self.config.workflows

    def workflow_paths(self) -> list[Path]:
        directory = self.workflow_directory()

        if not directory.is_dir():
            return []

        return sorted(
            path
            for path in directory.rglob("*")
            if path.is_file()
            and path.suffix.lower() in {".yaml", ".yml", ".json"}
        )

    def knowledge_directory(self) -> Path:
        return self.root / self.config.knowledge

    def knowledge_paths(self) -> list[Path]:
        directory = self.knowledge_directory()

        if not directory.is_dir():
            return []

        return sorted(
            path
            for path in directory.rglob("*")
            if path.is_file()
            and path.suffix.lower()
            in {
                ".txt",
                ".md",
                ".pdf",
                ".html",
                ".htm",
            }
        )


    def agent_directory(self) -> Path:
        return self.root / self.config.agents

    def agent_paths(self) -> list[Path]:
        directory = self.agent_directory()

        if not directory.is_dir():
            return []

        return sorted(
            path
            for path in directory.rglob("*")
            if path.is_file()
            and path.suffix.lower() in {".yaml", ".yml"}
        )

    def list_agents(self) -> list[AgentSummary]:
        loader = AgentDefinitionLoader()
        agents: list[AgentSummary] = []

        for path in self.agent_paths():
            definition = loader.load(path)

            agents.append(
                AgentSummary(
                    id=definition.id,
                    name=definition.name,
                    path=path,
                )
            )

        return agents

    def load_agent(
        self,
        path: str | Path,
    ) -> AgentDefinition:
        agent_path = self._project_path(path)

        return AgentDefinitionLoader().load(
            agent_path,
        )

    def save_agent(
        self,
        agent: AgentDefinition,
        path: str | Path | None = None,
    ) -> Path:
        if path is None:
            path = self.agent_directory() / f"{agent.id}.yaml"

        agent_path = self._project_path(path)

        if agent_path.suffix.lower() not in {".yaml", ".yml"}:
            raise ValueError(
                "Agent definitions must use .yaml or .yml files."
            )

        return AgentDefinitionLoader().save(
            agent,
            agent_path,
        )

    def delete_agent(
        self,
        path: str | Path,
    ) -> Path:
        agent_path = self._project_path(path)

        if not agent_path.is_file():
            raise FileNotFoundError(
                f"Agent file not found: {agent_path}"
            )

        agent_path.unlink()

        return agent_path

    def form_directory(self) -> Path:
        return self.root / self.config.forms

    def form_paths(self) -> list[Path]:
        directory = self.form_directory()

        if not directory.is_dir():
            return []

        return sorted(
            path
            for path in directory.rglob("*")
            if path.is_file()
            and path.suffix.lower() in {".yaml", ".yml", ".json"}
        )

    def list_forms(self) -> list[FormSummary]:
        forms: list[FormSummary] = []

        for path in self.form_paths():
            definition = self.load_form(path)

            forms.append(
                FormSummary(
                    id=definition.id,
                    name=definition.name,
                    path=path,
                )
            )

        return forms

    def load_form(
        self,
        path: str | Path,
    ) -> FormDefinition:
        form_path = self._project_path(path)

        import json
        import yaml

        if form_path.suffix.lower() == ".json":
            data = json.loads(
                form_path.read_text(
                    encoding="utf-8",
                )
            )
        else:
            data = yaml.safe_load(
                form_path.read_text(
                    encoding="utf-8",
                )
            )

        return FormDefinition.from_dict(data)

    def save_form(
        self,
        form: FormDefinition,
        path: str | Path | None = None,
    ) -> Path:
        if path is None:
            path = self.form_directory() / f"{form.id}.yaml"

        form_path = self._project_path(path)

        if form_path.suffix.lower() not in {
            ".yaml",
            ".yml",
            ".json",
        }:
            raise ValueError(
                "Form definitions must use .yaml, .yml, or .json files."
            )

        form_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = form.to_dict()

        if form_path.suffix.lower() == ".json":
            import json

            form_path.write_text(
                json.dumps(
                    data,
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        else:
            import yaml

            form_path.write_text(
                yaml.safe_dump(
                    data,
                    sort_keys=False,
                    allow_unicode=True,
                ),
                encoding="utf-8",
            )

        return form_path

    def delete_form(
        self,
        path: str | Path,
    ) -> Path:
        form_path = self._project_path(path)

        if not form_path.is_file():
            raise FileNotFoundError(
                f"Form file not found: {form_path}"
            )

        form_path.unlink()

        return form_path

    def load_workflow(
        self,
        path: str | Path,
    ) -> WorkflowDefinition:
        workflow_path = self._project_path(path)

        return WorkflowDefinitionLoader().load(
            workflow_path,
            strict=False,
        )

    def save_workflow(
        self,
        workflow: WorkflowDefinition,
        path: str | Path | None = None,
    ) -> Path:
        if path is None:
            path = self.workflow_directory() / f"{workflow.id}.yaml"

        workflow_path = self._project_path(path)

        workflow_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        import yaml

        data = workflow.to_dict()

        workflow_path.write_text(
            yaml.safe_dump(
                data,
                sort_keys=False,
                allow_unicode=True,
            ),
            encoding="utf-8",
        )

        return workflow_path

    def delete_workflow(
        self,
        path: str | Path,
    ) -> Path:
        workflow_path = self._project_path(path)

        if not workflow_path.is_file():
            raise FileNotFoundError(
                f"Workflow file not found: {workflow_path}"
            )

        workflow_path.unlink()

        return workflow_path

    def copy_to(
        self,
        destination: str | Path,
    ) -> "ProjectRepository":
        destination_path = Path(destination).expanduser().resolve()

        if destination_path.exists():
            raise FileExistsError(
                f"Destination already exists: {destination_path}"
            )

        copytree(
            self.root,
            destination_path,
        )

        return ProjectRepository(destination_path)

    def _project_path(
        self,
        path: str | Path,
    ) -> Path:
        candidate = Path(path)

        if not candidate.is_absolute():
            candidate = self.root / candidate

        candidate = candidate.resolve()

        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise ValueError(
                f"Path must remain inside project directory: {candidate}"
            ) from exc

        return candidate

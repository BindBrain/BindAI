from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bindai_agent import AgentDefinition, AgentRegistry
from bindai_project import Project, ProjectConfiguration
from bindai_agent.definition.builder import build_agent
from bindai_core.context import ExecutionContext
from bindai_memory import Memory
from bindai_memory.providers.sqlite import SQLiteMemoryProvider
from bindai_retrieval import (
    MemoryRetrieverProvider,
    Retriever,
)
from bindai_connections import ConnectionManifest, KeyringProviderCredentialStore
from bindai_knowledge import (
    DirectoryLoader,
    InMemoryKnowledgeProvider,
    Knowledge,
)
from bindai_config.tool_loader import ToolLoader
from bindai_tool import ToolRegistry
from bindai_workflow import (
    DefinitionDiagnostic,
    FileWorkflowStore,
    WorkflowDefinition,
    WorkflowDefinitionRuntime,
    WorkflowDefinitionValidator,
)

from .connection_tools import WebhookConnectionTool
from .forms import FormDefinition
from .repository import (
    AgentSummary,
    FormSummary as RepositoryFormSummary,
    ProjectRepository,
)


@dataclass(frozen=True, slots=True)
class ProjectSummary:
    name: str
    path: Path
    workflow_count: int
    agent_count: int
    form_count: int


@dataclass(frozen=True, slots=True)
class WorkflowSummary:
    id: str
    name: str
    path: Path


@dataclass(frozen=True, slots=True)
class StudioFormSummary:
    id: str
    name: str
    path: Path


class ProjectStudioService:
    """
    Filesystem-backed application service for BindAI Studio.

    Studio operates on portable project files through ProjectRepository.
    It does not replace the existing runtime Project or WorkflowRegistry.

    Runtime loading is intentionally explicit: Studio loads project resources
    into the existing AgentRegistry before building an executable workflow.

    It does not create a second execution engine.

    Runtime workflows are retained by this service so the existing
    WorkflowExecutor and MemoryWorkflowStore remain available across HTTP
    requests. This is required for paused HumanTaskNode workflows.
    """

    def __init__(
        self,
        project_root: str | Path,
    ):
        self.project = ProjectRepository(project_root)
        self.connections = ConnectionManifest(
            self.project.root / ".bindai" / "connections.toml",
        )

        self.credentials = KeyringProviderCredentialStore()
        if not self.project.is_project():
            raise ValueError(
                f"Not a BindAI project: {self.project.root}"
            )

        self._runtime_workflows: dict[str, object] = {}

        self._runtime_project = Project(
            ProjectConfiguration(
                name=self.project.config.name or self.project.root.name,
            )
        )

    @classmethod
    def discover_projects(
        cls,
        parent: str | Path,
    ) -> list[ProjectSummary]:
        return cls.discover(parent)

    @classmethod
    def discover(
        cls,
        parent: str | Path,
    ) -> list[ProjectSummary]:
        return [
            ProjectSummary(
                name=repository.config.name,
                path=repository.root,
                workflow_count=len(
                    repository.workflow_paths()
                ),
                agent_count=len(
                    repository.agent_paths()
                ),
                form_count=len(
                    repository.form_paths()
                ),
            )
            for repository in ProjectRepository.discover(
                parent
            )
        ]
    def summary(self) -> ProjectSummary:
        return ProjectSummary(
            name=self.project.config.name,
            path=self.project.root,
            workflow_count=len(
                self.project.workflow_paths()
            ),
            agent_count=len(
                self.project.agent_paths()
            ),
            form_count=len(
                self.project.form_paths()
            ),
        )


    def list_workflows(
        self,
    ) -> list[WorkflowSummary]:
        workflows: list[WorkflowSummary] = []

        for path in self.project.workflow_paths():
            workflow = self.project.load_workflow(path)

            workflows.append(
                WorkflowSummary(
                    id=workflow.id,
                    name=workflow.name,
                    path=path,
                )
            )

        return workflows

    def load_workflow(
        self,
        path: str | Path,
    ) -> WorkflowDefinition:
        return self.project.load_workflow(path)

    def save_workflow(
        self,
        workflow: WorkflowDefinition,
        path: str | Path | None = None,
    ) -> Path:
        self._runtime_workflows.pop(
            workflow.id,
            None,
        )

        return self.project.save_workflow(
            workflow,
            path,
        )

    def validate_workflow(
        self,
        workflow: WorkflowDefinition,
    ) -> list[DefinitionDiagnostic]:
        return WorkflowDefinitionValidator().validate(
            workflow,
        )

    def delete_workflow(
        self,
        workflow_id: str,
    ) -> Path:
        for path in self.project.workflow_paths():
            workflow = self.project.load_workflow(path)

            if workflow.id != workflow_id:
                continue

            self._runtime_workflows.pop(
                workflow_id,
                None,
            )

            return self.project.delete_workflow(path)

        raise FileNotFoundError(
            f"Workflow '{workflow_id}' was not found."
        )
    def list_agents(
        self,
    ) -> list[AgentSummary]:
        return self.project.list_agents()

    def load_agent(
        self,
        path: str | Path,
    ) -> AgentDefinition:
        return self.project.load_agent(path)

    def save_agent(
        self,
        agent: AgentDefinition,
        path: str | Path | None = None,
    ) -> Path:
        return self.project.save_agent(
            agent,
            path,
        )

    def find_agent_references(
        self,
        agent_id: str,
    ) -> list[dict[str, str]]:
        references: list[dict[str, str]] = []

        for path in self.project.workflow_paths():
            workflow = self.project.load_workflow(path)

            for node in workflow.nodes:
                configuration = node.configuration

                if (
                    node.type.lower()
                    in {
                        "agent",
                        "agentnode",
                    }
                    and configuration.get("agent")
                    == agent_id
                ):
                    references.append(
                        {
                            "workflow_id": workflow.id,
                            "workflow_name": workflow.name,
                            "node_id": node.id,
                            "node_name": node.name or node.id,
                        }
                    )

        return references
    def delete_agent(
        self,
        agent_id: str,
    ) -> Path:
        references = self.find_agent_references(
            agent_id,
        )

        if references:
            workflows = ", ".join(
                reference["workflow_name"]
                for reference in references
            )

            raise ValueError(
                f"Agent '{agent_id}' is referenced by "
                f"workflow(s): {workflows}."
            )

        for path in self.project.agent_paths():
            agent = self.project.load_agent(path)

            if agent.id != agent_id:
                continue

            return self.project.delete_agent(path)

        raise FileNotFoundError(
            f"Agent '{agent_id}' was not found."
        )

    def list_forms(
        self,
    ) -> list[StudioFormSummary]:
        forms: list[StudioFormSummary] = []

        for form in self.project.list_forms():
            forms.append(
                StudioFormSummary(
                    id=form.id,
                    name=form.name,
                    path=form.path,
                )
            )

        return forms

    def list_knowledge(
        self,
    ) -> list[dict[str, str]]:
        return [
            {
                "id": path.stem,
                "name": path.name,
                "path": str(path),
                "type": path.suffix.lower().lstrip("."),
            }
            for path in self.project.knowledge_paths()
        ]


    def load_form(
        self,
        path: str | Path,
    ) -> FormDefinition:
        return self.project.load_form(path)

    def save_form(
        self,
        form: FormDefinition,
        path: str | Path | None = None,
    ) -> Path:
        return self.project.save_form(
            form,
            path,
        )

    def find_form_references(
        self,
        form_id: str,
    ) -> list[dict[str, str]]:
        references: list[dict[str, str]] = []

        for path in self.project.workflow_paths():
            workflow = self.project.load_workflow(path)

            for node in workflow.nodes:
                configuration = node.configuration
                node_type = node.type.lower()

                if (
                    node_type
                    in {
                        "humantask",
                        "human_task",
                        "humantasknode",
                    }
                    and configuration.get("form")
                    == form_id
                ):
                    references.append(
                        {
                            "workflow_id": workflow.id,
                            "workflow_name": workflow.name,
                            "node_id": node.id,
                            "node_name": node.name or node.id,
                        }
                    )

        return references
    def delete_form(
        self,
        form_id: str,
    ) -> Path:
        references = self.find_form_references(
            form_id,
        )

        if references:
            workflows = ", ".join(
                reference["workflow_name"]
                for reference in references
            )

            raise ValueError(
                f"Form '{form_id}' is referenced by "
                f"workflow(s): {workflows}."
            )

        for path in self.project.form_paths():
            form = self.project.load_form(path)

            if form.id != form_id:
                continue

            return self.project.delete_form(path)

        raise FileNotFoundError(
            f"Form '{form_id}' was not found."
        )

    def list_connections(self):
        return self.connections.list()

    def save_connection(self, name: str, provider: str):
        if provider != "webhook":
            raise ValueError(
                f"Connection provider '{provider}' is not supported in Studio V1."
            )

        self.connections.add(name, provider)
        self._runtime_workflows.clear()

        return self.connections.get(name)

    def delete_connection(self, name: str) -> None:
        self.delete_connection_credential(name)
        self.connections.remove(name)
        self._runtime_workflows.clear()

    def set_connection_credential(self, name: str, credential: str) -> None:
        connection = self.connections.get(name)

        if connection is None:
            raise ValueError(
                f"Connection '{name}' does not exist."
            )

        self.credentials.set(connection.name, credential)

    def delete_connection_credential(self, name: str) -> None:
        connection = self.connections.get(name)

        if connection is None:
            return

        self.credentials.delete(connection.name)
    def send_connection(
        self,
        name: str,
        payload: object,
    ) -> object:
        connection = self.connections.get(name)

        if connection is None:
            raise ValueError(
                f"Connection '{name}' does not exist."
            )

        if connection.provider != "webhook":
            raise ValueError(
                f"Connection provider '{connection.provider}' is not supported in Studio V1."
            )

        credential = self.credentials.get(connection.name)

        if not credential:
            raise ValueError(
                f"Connection '{name}' has no configured credential."
            )

        from bindai_connections import (
            ConnectionManager,
            ConnectionRegistry,
        )

        provider = ConnectionRegistry.provider(connection.provider)
        runtime_connection = provider(credential)

        manager = ConnectionManager()
        manager.add(runtime_connection)

        try:
            manager.connect(runtime_connection.name)
            return runtime_connection.send(payload)
        finally:
            manager.disconnect(runtime_connection.name)

    def load_runtime_agents(
        self,
        *,
        clear_registry: bool = False,
    ) -> list[object]:
        if clear_registry:
            AgentRegistry.clear()

        agents: list[object] = []

        for path in self.project.agent_paths():
            definition = self.project.load_agent(path)

            memory = None

            if definition.memory is not None:
                memory_directory = (
                    self.project.root
                    / self.project.config.memory
                )

                memory_directory.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                memory_database = (
                    memory_directory
                    / f"{definition.memory}.db"
                )

                memory = Memory(
                    SQLiteMemoryProvider(
                        str(memory_database),
                    ),
                )

            retriever = None

            if definition.retriever is not None:
                if memory is None:
                    raise ValueError(
                        f"Agent '{definition.id}' references retriever "
                        f"'{definition.retriever}', but no memory resource was provided."
                    )

                retriever = Retriever(
                    MemoryRetrieverProvider(
                        memory,
                    ),
                )

            knowledge = None

            if definition.knowledge is not None:
                knowledge_directory = (
                    self.project.root
                    / self.project.config.knowledge
                )

                knowledge_directory.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                knowledge = Knowledge(
                    InMemoryKnowledgeProvider(),
                )

                knowledge.load(
                    DirectoryLoader(
                        str(knowledge_directory),
                    ),
                )

            agent = build_agent(
                definition,
                project_root=self.project.root,
                memory=memory,
                retriever=retriever,
                knowledge=knowledge,
            )

            agents.append(agent)

        return agents

    def list_tools(
        self,
    ) -> list[dict[str, object]]:
        from .connection_tools import WebhookConnectionTool

        tools = [
            {
                "id": tool.name,
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.definition.parameters,
            }
            for tool in ToolLoader.load(
                self.project.root,
            )
        ]

        for connection in self.connections.list():
            if connection.provider != "webhook":
                continue

            tool = WebhookConnectionTool(
                connection.name,
                self.send_connection,
            )

            tools.append({
                "id": tool.name,
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.definition.parameters,
            })

        return tools

    def build_runtime_workflow(
        self,
        workflow: WorkflowDefinition,
        *,
        load_agents: bool = True,
        clear_registry: bool = False,
    ):
        existing = self._runtime_workflows.get(
            workflow.id,
        )

        if existing is not None:
            return existing

        if load_agents:
            self.load_runtime_agents(
                clear_registry=clear_registry,
            )

        tool_registry = ToolRegistry()

        for tool in ToolLoader.load(
            self.project.root,
        ):
            tool_registry.register(tool)

        from .connection_tools import WebhookConnectionTool

        for connection in self.connections.list():
            if connection.provider != "webhook":
                continue

            tool_registry.register(
                WebhookConnectionTool(
                    connection.name,
                    self.send_connection,
                ),
            )


        workflow_store = FileWorkflowStore(
            self.project.root / ".bindai" / "workflow-runs",
            self._resolve_runtime_workflow,
        )

        runtime = WorkflowDefinitionRuntime(
            tool_registry=tool_registry,
            store=workflow_store,
        )

        executable = runtime.build(
            workflow,
        )

        self._runtime_workflows[workflow.id] = executable
        self._runtime_project.add_workflow(
            executable,
        )

        return executable

    def _resolve_runtime_workflow(
        self,
        workflow_id: str,
        version: int,
    ) -> WorkflowDefinition | None:
        for summary in self.list_workflows():
            workflow = self.project.load_workflow(
                summary.path,
            )

            if workflow.id == workflow_id and workflow.version == version:
                return self.build_runtime_workflow(
                    workflow,
                    load_agents=True,
                )

        return None

    def execute_runtime_workflow(
        self,
        workflow: WorkflowDefinition,
        *,
        variables: dict[str, Any] | None = None,
        clear_registry: bool = False,
    ):
        # Build every project workflow so SubWorkflow nodes can resolve
        # their child workflows through the runtime Project.
        for workflow_summary in self.list_workflows():
            workflow_definition = self.project.load_workflow(
                workflow_summary.path,
            )

            self.build_runtime_workflow(
                workflow_definition,
                load_agents=True,
                clear_registry=clear_registry,
            )

        executable = self.build_runtime_workflow(
            workflow,
            load_agents=True,
            clear_registry=clear_registry,
        )

        context = ExecutionContext()

        if variables:
            context.variables.update(
                variables,
            )

        instance = executable.create_instance()
        instance.project = self._runtime_project

        instance.context.variables.update(
            context.variables,
        )

        instance.context.metadata.update(
            context.metadata,
        )

        return executable.executor.execute(
            instance,
        )

    def simulate_runtime_workflow(
        self,
        workflow: WorkflowDefinition,
        *,
        variables: dict[str, Any] | None = None,
        clear_registry: bool = False,
    ):
        executable = self.build_runtime_workflow(
            workflow,
            load_agents=True,
            clear_registry=clear_registry,
        )

        context = ExecutionContext()

        if variables:
            context.variables.update(
                variables,
            )

        context.metadata["bindai_simulation"] = True

        return executable.run(
            context,
        )

    def get_runtime_workflow(
        self,
        workflow_id: str,
    ):
        return self._runtime_workflows.get(
            workflow_id,
        )

    def resume_runtime_workflow(
        self,
        workflow_id: str,
        instance_id: str,
        action: str,
    ):
        executable = self._runtime_workflows.get(
            workflow_id,
        )

        if executable is None:
            workflow_definition = None

            for summary in self.list_workflows():
                candidate = self.project.load_workflow(
                    summary.path,
                )

                if candidate.id == workflow_id:
                    workflow_definition = candidate
                    break

            if workflow_definition is None:
                raise ValueError(
                    f"Workflow '{workflow_id}' was not found."
                )

            executable = self.build_runtime_workflow(
                workflow_definition,
                load_agents=True,
            )

        executor = executable.executor

        instance = executor.store.load(
            instance_id,
        )

        if instance is None:
            raise ValueError(
                f"Workflow instance '{instance_id}' was not found."
            )

        if not getattr(
            instance.context,
            "waiting",
            False,
        ):
            raise ValueError(
                f"Workflow instance '{instance_id}' is not waiting for human input."
            )

        task = getattr(
            instance.context,
            "task",
            None,
        )

        if task is None:
            raise ValueError(
                f"Workflow instance '{instance_id}' has no human task."
            )

        action = action.strip().lower()

        if action == "approved":
            task.approve()
        elif action == "rejected":
            task.reject()
        else:
            raise ValueError(
                "Human task action must be 'approved' or 'rejected'."
            )

        return executor.resume(
            instance,
        )

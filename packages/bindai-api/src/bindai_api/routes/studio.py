from __future__ import annotations

import re
from pathlib import Path
from datetime import datetime
from typing import Any

from bindai_connections import ConnectionRegistry
from bindai_core.context import Variables
from bindai_tool import ToolResult
from bindai_providers import ProviderRegistry, bootstrap
from bindai_project import (
    FormDefinition,
    ProjectStudioService,
    ProjectWorkspace,
)
from bindai_workflow import FileWorkflowStore, WorkflowDefinition
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from ..auth import require_api_key
from ..studio_models import (
    StudioAgentCreateRequest,
    StudioAgentCreateResponse,
    StudioAgentDefinitionRequest,
    StudioAgentDefinitionResponse,
    StudioAgentResponse,
    StudioConnectionCreateRequest,
    StudioConnectionCredentialRequest,
    StudioConnectionResponse,
    StudioDiagnosticResponse,
    StudioFormCreateRequest,
    StudioFormCreateResponse,
    StudioFormDefinitionRequest,
    StudioFormDefinitionResponse,
    StudioFormResponse,
    StudioHumanTaskResponse,
    StudioProjectCreateRequest,
    StudioProjectCreateResponse,
    StudioProjectResponse,
    StudioToolResponse,
    StudioKnowledgeResponse,
    StudioWorkflowCreateRequest,
    StudioWorkflowCreateResponse,
    StudioWorkflowDefinitionRequest,
    StudioWorkflowHumanTaskRequest,
    StudioWorkflowResponse,
    StudioWorkflowRunRequest,
    StudioWorkflowRunResponse,
    StudioWorkflowSaveResponse,
)


router = APIRouter(
    prefix="/api/v1/studio",
    tags=["studio"],
    dependencies=[Depends(require_api_key)],
)


_project_roots: dict[str, Path] = {}
_workspace_root: Path | None = None

# Keep the same ProjectStudioService instance alive across HTTP requests.
#
# This is important because ProjectStudioService retains the executable
# Workflow, and that Workflow owns the WorkflowExecutor and its
# MemoryWorkflowStore. HumanTask workflows must be resumed through that
# same runtime object.
_studio_services: dict[str, ProjectStudioService] = {}


def configure_studio_workspace(
    workspace_root: str | Path,
) -> None:
    global _workspace_root

    root = Path(workspace_root).expanduser().resolve()

    if not root.is_dir():
        raise ValueError(
            f"Studio workspace directory does not exist: {root}"
        )

    _workspace_root = root


def clear_studio_workspace() -> None:
    global _workspace_root
    _workspace_root = None


def get_studio_workspace() -> ProjectWorkspace:
    if _workspace_root is None:
        raise HTTPException(
            status_code=500,
            detail="Studio workspace is not configured.",
        )

    return ProjectWorkspace(_workspace_root)


def configure_studio_project(
    project_id: str,
    project_root: str | Path,
) -> None:
    global _workspace_root

    root = Path(project_root).expanduser().resolve()

    if not root.is_dir():
        raise ValueError(
            f"Studio project directory does not exist: {root}"
        )

    _project_roots[project_id] = root
    _workspace_root = root.parent

    # If the project is reconfigured to another directory, do not retain
    # an executable runtime belonging to the previous project root.
    _studio_services.pop(project_id, None)


def clear_studio_projects() -> None:
    _project_roots.clear()
    _studio_services.clear()
    clear_studio_workspace()


def get_studio_project(
    project_id: str,
) -> ProjectStudioService:
    cached = _studio_services.get(project_id)

    if cached is not None:
        return cached

    root: Path | None = None

    if _workspace_root is not None:
        workspace = get_studio_workspace()

        for repository in workspace.discover():
            if repository.root.name == project_id:
                root = repository.root
                break

    if root is None:
        root = _project_roots.get(project_id)

    if root is None:
        raise HTTPException(
            status_code=404,
            detail=f"Studio project '{project_id}' was not found.",
        )

    try:
        service = ProjectStudioService(root)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    _studio_services[project_id] = service

    return service


def diagnostic_response(
    diagnostic,
) -> StudioDiagnosticResponse:
    return StudioDiagnosticResponse(
        severity=diagnostic.severity,
        code=diagnostic.code,
        message=diagnostic.message,
        node_id=diagnostic.node_id,
        node_type=diagnostic.node_type,
        suggestion=diagnostic.suggestion,
    )


def studio_json_value(value: Any) -> Any:
    """
    Convert BindAI runtime values into JSON-safe Studio API values.

    The workflow runtime is allowed to return rich Python objects. The Studio
    HTTP API must expose a portable JSON representation without changing the
    runtime's execution contracts.
    """
    if isinstance(value, ToolResult):
        if not value.success:
            return {
                "success": False,
                "error": value.error,
            }

        return studio_json_value(value.value)

    if isinstance(value, Variables):
        return {
            key: studio_json_value(item)
            for key, item in value.items()
        }

    if isinstance(value, dict):
        return {
            str(key): studio_json_value(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            studio_json_value(item)
            for item in value
        ]

    if isinstance(value, set):
        return [
            studio_json_value(item)
            for item in value
        ]

    return value


def studio_result_response(
    result: Any,
) -> dict[str, Any]:
    """
    Convert a BindAI ExecutionResult/WorkflowResult into a JSON-safe payload.
    """
    return {
        "success": bool(result.success),
        "output": studio_json_value(result.output),
        "error": result.error,
    }


def studio_human_task_response(
    task: Any,
) -> StudioHumanTaskResponse:
    created_at = getattr(task, "created_at", None)

    if created_at is None:
        created_at_value = ""
    elif hasattr(created_at, "isoformat"):
        created_at_value = created_at.isoformat()
    else:
        created_at_value = str(created_at)

    return StudioHumanTaskResponse(
        id=str(task.id),
        node_id=str(task.node_id),
        assignee=getattr(task, "assignee", None),
        role=getattr(task, "role", None),
        completed=bool(getattr(task, "completed", False)),
        result=getattr(task, "result", None),
        created_at=created_at_value,
    )


def find_workflow_instance(
    service: ProjectStudioService,
    workflow_id: str,
    instance_ids: set[str] | None = None,
):
    """
    Find a runtime WorkflowInstance in the retained WorkflowExecutor store.
    If instance_ids is supplied, only those instances are considered.
    """
    runtime_workflow = service.get_runtime_workflow(workflow_id)

    if runtime_workflow is None:
        return None

    store = runtime_workflow.executor.store

    if isinstance(store, FileWorkflowStore):
        if instance_ids:
            for instance_id in instance_ids:
                instance = store.load(instance_id)
                if instance is not None:
                    return instance
            return None

        candidates = []

        for path in store.root.glob("*.json"):
            instance = store.load(path.stem)

            if instance is None:
                continue

            if getattr(instance, "workflow_id", None) != workflow_id:
                continue

            candidates.append(instance)

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda instance: getattr(
                instance.context,
                "started_at",
                datetime.min,
            ),
        )

    instances = getattr(store, "instances", {})

    candidates = []

    for instance_id, instance in instances.items():
        if (
            instance_ids is not None
            and instance_id not in instance_ids
        ):
            continue

        candidates.append(instance)

    if not candidates:
        return None

    return candidates[-1]

def studio_run_response(
    service: ProjectStudioService,
    workflow_id: str,
    result: Any,
    instance_ids: set[str] | None = None,
) -> StudioWorkflowRunResponse:
    instance = find_workflow_instance(
        service,
        workflow_id,
        instance_ids=instance_ids,
    )

    if instance is None:
        return StudioWorkflowRunResponse(
            workflow=workflow_id,
            instance_id=None,
            waiting=False,
            human_task=None,
            result=studio_result_response(result),
        )

    context = instance.context
    waiting = bool(getattr(context, "waiting", False))
    task = getattr(context, "task", None)

    return StudioWorkflowRunResponse(
        workflow=workflow_id,
        instance_id=str(instance.id),
        waiting=waiting,
        human_task=(
            studio_human_task_response(task)
            if task is not None
            else None
        ),
        result=studio_result_response(result),
    )


def slugify_workflow_name(
    name: str,
) -> str:
    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        name.strip().lower(),
    ).strip("-")

    if not value:
        raise ValueError(
            "Workflow name must contain at least one letter or number."
        )

    return value


def make_unique_workflow_id(
    name: str,
    existing_ids: set[str],
) -> str:
    base = slugify_workflow_name(name)

    if base not in existing_ids:
        return base

    suffix = 2

    while f"{base}-{suffix}" in existing_ids:
        suffix += 1

    return f"{base}-{suffix}"


def slugify_agent_name(
    name: str,
) -> str:
    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        name.strip().lower(),
    ).strip("-")

    if not value:
        raise ValueError(
            "Agent name must contain at least one letter or number."
        )

    return value


def make_unique_agent_id(
    name: str,
    existing_ids: set[str],
) -> str:
    base = slugify_agent_name(name)

    if base not in existing_ids:
        return base

    suffix = 2

    while f"{base}-{suffix}" in existing_ids:
        suffix += 1

    return f"{base}-{suffix}"


def slugify_form_name(
    name: str,
) -> str:
    value = re.sub(
        r"[^a-z0-9]+",
        "-",
        name.strip().lower(),
    ).strip("-")

    if not value:
        raise ValueError(
            "Form name must contain at least one letter or number."
        )

    return value


def make_unique_form_id(
    name: str,
    existing_ids: set[str],
) -> str:
    base = slugify_form_name(name)

    if base not in existing_ids:
        return base

    suffix = 2

    while f"{base}-{suffix}" in existing_ids:
        suffix += 1

    return f"{base}-{suffix}"


def validate_agent_id(
    agent_id: str,
) -> str:
    value = agent_id.strip()

    if not value:
        raise ValueError("Agent ID cannot be empty.")

    if not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]*",
        value,
    ):
        raise ValueError(
            "Agent ID may contain only letters, numbers, "
            "dots, underscores, and hyphens."
        )

    return value


@router.get(
    "/projects",
    response_model=list[StudioProjectResponse],
)
def list_studio_projects():
    workspace = get_studio_workspace()
    projects = []

    for repository in workspace.discover():
        service = ProjectStudioService(repository.root)
        summary = service.summary()

        projects.append(
            StudioProjectResponse(
                name=summary.name,
                path=str(summary.path),
                workflow_count=summary.workflow_count,
                agent_count=summary.agent_count,
                form_count=summary.form_count,
            )
        )

    return projects


@router.get("/providers")
def list_studio_providers() -> list[str]:
    bootstrap()
    return ProviderRegistry.list()

@router.get("/capabilities")
def list_studio_capabilities() -> list[dict]:
    from bindai_workflow import default_capability_registry

    return default_capability_registry.to_dict()


@router.post(
    "/projects",
    response_model=StudioProjectCreateResponse,
    status_code=201,
)
def create_studio_project(
    payload: StudioProjectCreateRequest,
):
    workspace = get_studio_workspace()

    try:
        repository = workspace.create_project(payload.name)
    except FileExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return StudioProjectCreateResponse(
        name=repository.config.name,
        path=str(repository.root),
        workflow_count=len(repository.workflow_paths()),
        agent_count=len(repository.agent_paths()),
        form_count=len(repository.form_paths()),
    )


@router.get(
    "/projects/{project_id}",
    response_model=StudioProjectResponse,
)
def get_studio_project_summary(
    project_id: str,
) -> StudioProjectResponse:
    service = get_studio_project(project_id)
    summary = service.summary()

    return StudioProjectResponse(
        name=summary.name,
        path=str(summary.path),
        workflow_count=summary.workflow_count,
        agent_count=summary.agent_count,
        form_count=summary.form_count,
    )


@router.get(
    "/projects/{project_id}/agents",
    response_model=list[StudioAgentResponse],
)
def list_studio_agents(
    project_id: str,
) -> list[StudioAgentResponse]:
    service = get_studio_project(project_id)

    return [
        StudioAgentResponse(
            id=agent.id,
            name=agent.name,
            path=str(agent.path),
        )
        for agent in service.list_agents()
    ]

@router.get(
    "/projects/{project_id}/knowledge",
    response_model=list[StudioKnowledgeResponse],
)
def list_studio_knowledge(
    project_id: str,
) -> list[StudioKnowledgeResponse]:
    service = get_studio_project(project_id)

    return [
        StudioKnowledgeResponse(
            id=item["id"],
            name=item["name"],
            path=item["path"],
            type=item["type"],
        )
        for item in service.list_knowledge()
    ]

@router.post(
    "/projects/{project_id}/knowledge",
    response_model=StudioKnowledgeResponse,
)
def upload_studio_knowledge(
    project_id: str,
    file: UploadFile = File(...),
) -> StudioKnowledgeResponse:
    service = get_studio_project(project_id)

    filename = Path(file.filename or "").name
    suffix = Path(filename).suffix.lower()

    allowed_suffixes = {
        ".txt",
        ".md",
        ".pdf",
        ".html",
        ".htm",
    }

    if not filename or suffix not in allowed_suffixes:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported knowledge file type. "
                "Supported types: .txt, .md, .pdf, .html, .htm."
            ),
        )

    knowledge_directory = (
        service.project.knowledge_directory()
    )
    knowledge_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = knowledge_directory / filename

    destination.write_bytes(
        file.file.read(),
    )

    return StudioKnowledgeResponse(
        id=destination.stem,
        name=destination.name,
        path=str(destination),
        type=suffix.lstrip("."),
    )

@router.get(
    "/projects/{project_id}/tools",
    response_model=list[StudioToolResponse],
)
def list_studio_tools(
    project_id: str,
) -> list[StudioToolResponse]:
    service = get_studio_project(project_id)

    return [
        StudioToolResponse(
            id=tool["id"],
            name=tool["name"],
            description=tool["description"],
            parameters=tool.get("parameters", {}),
        )
        for tool in service.list_tools()
    ]


@router.post(
    "/projects/{project_id}/agents",
    response_model=StudioAgentCreateResponse,
    status_code=201,
)
def create_studio_agent(
    project_id: str,
    payload: StudioAgentCreateRequest,
) -> StudioAgentCreateResponse:
    service = get_studio_project(project_id)
    name = payload.name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Agent name is required.",
        )

    existing_ids = {
        agent.id
        for agent in service.list_agents()
    }

    try:
        if payload.id:
            agent_id = validate_agent_id(payload.id)

            if agent_id in existing_ids:
                raise HTTPException(
                    status_code=409,
                    detail=f"Agent '{agent_id}' already exists.",
                )
        else:
            agent_id = make_unique_agent_id(
                name,
                existing_ids,
            )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    try:
        from bindai_agent import AgentDefinition

        definition = AgentDefinition(
            id=agent_id,
            name=name,
        )

        path = service.save_agent(definition)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return StudioAgentCreateResponse(
        agent=definition.to_dict(),
        path=str(path),
    )


@router.get(
    "/projects/{project_id}/agents/{agent_id}",
    response_model=StudioAgentDefinitionResponse,
)
def get_studio_agent(
    project_id: str,
    agent_id: str,
) -> StudioAgentDefinitionResponse:
    service = get_studio_project(project_id)

    for agent in service.list_agents():
        if agent.id == agent_id:
            definition = service.load_agent(agent.path)

            return StudioAgentDefinitionResponse(
                agent=definition.to_dict(),
            )

    raise HTTPException(
        status_code=404,
        detail=f"Agent '{agent_id}' was not found.",
    )


@router.put(
    "/projects/{project_id}/agents/{agent_id}",
    response_model=StudioAgentDefinitionResponse,
)
def save_studio_agent(
    project_id: str,
    agent_id: str,
    payload: StudioAgentDefinitionRequest,
) -> StudioAgentDefinitionResponse:
    service = get_studio_project(project_id)
    data = dict(payload.agent)

    if str(data.get("id", "")) != agent_id:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Agent body id '{data.get('id')}' "
                f"does not match URL agent id '{agent_id}'."
            ),
        )

    try:
        from bindai_agent import AgentDefinition

        definition = AgentDefinition.from_dict(data)

        print(
            "SAVE STUDIO AGENT",
            definition.to_dict(),
        )

        service.save_agent(definition)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return StudioAgentDefinitionResponse(
        agent=definition.to_dict(),
    )


@router.get("/connection-providers")
def list_studio_connection_providers() -> list[str]:
    return ["webhook"]

@router.get(
    "/projects/{project_id}/connections",
    response_model=list[StudioConnectionResponse],
)
def list_studio_connections(
    project_id: str,
) -> list[StudioConnectionResponse]:
    service = get_studio_project(project_id)

    return [
        StudioConnectionResponse(
            name=connection.name,
            provider=connection.provider,
        configured=service.credentials.exists(connection.name),
        )
        for connection in service.list_connections()
    ]


@router.post(
    "/projects/{project_id}/connections",
    response_model=StudioConnectionResponse,
)
def create_studio_connection(
    project_id: str,
    request: StudioConnectionCreateRequest,
) -> StudioConnectionResponse:
    service = get_studio_project(project_id)

    try:
        connection = service.save_connection(
            request.name,
            request.provider,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return StudioConnectionResponse(
        name=connection.name,
        provider=connection.provider,
        configured=service.credentials.exists(connection.name),
    )


@router.put(
    "/projects/{project_id}/connections/{connection_name}/credential",
)
def set_studio_connection_credential(
    project_id: str,
    connection_name: str,
    request: StudioConnectionCredentialRequest,
) -> dict[str, str]:
    service = get_studio_project(project_id)

    try:
        service.set_connection_credential(
            connection_name,
            request.credential,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "status": "configured",
        "name": connection_name,
    }

@router.delete(
    "/projects/{project_id}/connections/{connection_name}",
)
def delete_studio_connection(
    project_id: str,
    connection_name: str,
) -> dict[str, str]:
    service = get_studio_project(project_id)
    service.delete_connection(connection_name)

    return {
        "status": "deleted",
        "name": connection_name,
    }

@router.delete(
    "/projects/{project_id}/agents/{agent_id}",
)
def delete_studio_agent(
    project_id: str,
    agent_id: str,
) -> dict[str, str]:
    service = get_studio_project(project_id)

    try:
        service.delete_agent(agent_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return {
        "id": agent_id,
        "deleted": "true",
    }


@router.get(
    "/projects/{project_id}/forms",
    response_model=list[StudioFormResponse],
)
def list_studio_forms(
    project_id: str,
) -> list[StudioFormResponse]:
    service = get_studio_project(project_id)

    return [
        StudioFormResponse(
            id=form.id,
            name=form.name,
            path=str(form.path),
        )
        for form in service.list_forms()
    ]


@router.post(
    "/projects/{project_id}/forms",
    response_model=StudioFormCreateResponse,
    status_code=201,
)
def create_studio_form(
    project_id: str,
    payload: StudioFormCreateRequest,
) -> StudioFormCreateResponse:
    service = get_studio_project(project_id)
    name = payload.name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Form name cannot be empty.",
        )

    existing_forms = service.list_forms()

    existing_ids = {
        form.id
        for form in existing_forms
    }

    if payload.id:
        form_id = payload.id.strip()

        if not re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9._-]*",
            form_id,
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Form id may contain only letters, numbers, "
                    "dots, underscores, and hyphens."
                ),
            )

        if form_id in existing_ids:
            raise HTTPException(
                status_code=409,
                detail=f"Form '{form_id}' already exists.",
            )
    else:
        try:
            form_id = make_unique_form_id(
                name,
                existing_ids,
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

    definition = FormDefinition(
        id=form_id,
        name=name,
    )

    try:
        path = service.save_form(definition)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return StudioFormCreateResponse(
        form=definition.to_dict(),
        path=str(path),
    )


@router.get(
    "/projects/{project_id}/forms/{form_id}",
    response_model=StudioFormDefinitionResponse,
)
def get_studio_form(
    project_id: str,
    form_id: str,
) -> StudioFormDefinitionResponse:
    service = get_studio_project(project_id)

    for form in service.list_forms():
        if form.id == form_id:
            definition = service.load_form(form.path)

            return StudioFormDefinitionResponse(
                form=definition.to_dict(),
            )

    raise HTTPException(
        status_code=404,
        detail=f"Form '{form_id}' was not found.",
    )


@router.put(
    "/projects/{project_id}/forms/{form_id}",
    response_model=StudioFormDefinitionResponse,
)
def save_studio_form(
    project_id: str,
    form_id: str,
    payload: StudioFormDefinitionRequest,
) -> StudioFormDefinitionResponse:
    service = get_studio_project(project_id)
    data = dict(payload.form)

    if str(data.get("id", "")) != form_id:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Form body id '{data.get('id')}' "
                f"does not match URL form id '{form_id}'."
            ),
        )

    form_path: Path | None = None

    for form in service.list_forms():
        if form.id == form_id:
            form_path = form.path
            break

    if form_path is None:
        raise HTTPException(
            status_code=404,
            detail=f"Form '{form_id}' was not found.",
        )

    try:
        definition = FormDefinition.from_dict(
            {
                "version": data.get("version", 1),
                "form": data,
            }
        )

        print(
            "STUDIO FORM BEFORE SAVE:",
            definition.to_dict(),
        )

        service.save_form(
            definition,
            form_path,
        )
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return StudioFormDefinitionResponse(
        form=definition.to_dict(),
    )


@router.delete(
    "/projects/{project_id}/forms/{form_id}",
)
def delete_studio_form(
    project_id: str,
    form_id: str,
) -> dict[str, str]:
    service = get_studio_project(project_id)

    try:
        service.delete_form(form_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return {
        "id": form_id,
        "deleted": "true",
    }


@router.get(
    "/projects/{project_id}/workflows",
    response_model=list[StudioWorkflowResponse],
)
def list_studio_workflows(
    project_id: str,
) -> list[StudioWorkflowResponse]:
    service = get_studio_project(project_id)

    return [
        StudioWorkflowResponse(
            id=workflow.id,
            name=workflow.name,
            path=str(workflow.path),
        )
        for workflow in service.list_workflows()
    ]


@router.post(
    "/projects/{project_id}/workflows",
    response_model=StudioWorkflowCreateResponse,
    status_code=201,
)
def create_studio_workflow(
    project_id: str,
    payload: StudioWorkflowCreateRequest,
) -> StudioWorkflowCreateResponse:
    service = get_studio_project(project_id)
    name = payload.name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Workflow name cannot be empty.",
        )

    existing_workflows = service.list_workflows()

    existing_ids = {
        workflow.id
        for workflow in existing_workflows
    }

    try:
        workflow_id = payload.id or make_unique_workflow_id(
            payload.name,
            existing_ids,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    if workflow_id in existing_ids:
        raise HTTPException(
            status_code=409,
            detail=f"Workflow '{workflow_id}' already exists.",
        )

    if not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]*",
        workflow_id,
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Workflow id may contain only letters, numbers, "
                "dots, underscores, and hyphens."
            ),
        )

    definition = WorkflowDefinition(
        id=workflow_id,
        name=name,
    )

    path = service.save_workflow(definition)

    return StudioWorkflowCreateResponse(
        workflow=definition.to_dict(),
        path=str(path),
        diagnostics=[],
    )


@router.get(
    "/projects/{project_id}/workflows/{workflow_id}",
)
def get_studio_workflow(
    project_id: str,
    workflow_id: str,
) -> dict:
    service = get_studio_project(project_id)

    for workflow in service.list_workflows():
        if workflow.id == workflow_id:
            definition = service.load_workflow(workflow.path)
            return definition.to_dict()

    raise HTTPException(
        status_code=404,
        detail=f"Workflow '{workflow_id}' was not found.",
    )


@router.put(
    "/projects/{project_id}/workflows/{workflow_id}",
    response_model=StudioWorkflowSaveResponse,
)
def save_studio_workflow(
    project_id: str,
    workflow_id: str,
    payload: StudioWorkflowDefinitionRequest,
) -> StudioWorkflowSaveResponse:
    service = get_studio_project(project_id)

    workflow_path: Path | None = None

    for workflow in service.list_workflows():
        if workflow.id == workflow_id:
            workflow_path = workflow.path
            break

    if workflow_path is None:
        workflow_path = (
            service.project.workflow_directory()
            / f"{workflow_id}.yaml"
        )

    if payload.workflow.id != workflow_id:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Workflow body id '{payload.workflow.id}' "
                f"does not match URL workflow id '{workflow_id}'."
            ),
        )

    try:
        definition = WorkflowDefinition.from_dict(
            payload.to_definition_dict(),
            strict=False,
        )
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    diagnostics = service.validate_workflow(definition)

    service.save_workflow(
        definition,
        workflow_path,
    )

    return StudioWorkflowSaveResponse(
        workflow=definition.to_dict(),
        diagnostics=[
            diagnostic_response(diagnostic)
            for diagnostic in diagnostics
        ],
    )


@router.delete(
    "/projects/{project_id}/workflows/{workflow_id}",
)
def delete_studio_workflow(
    project_id: str,
    workflow_id: str,
) -> dict[str, str]:
    service = get_studio_project(project_id)

    try:
        service.delete_workflow(workflow_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return {
        "id": workflow_id,
        "deleted": "true",
    }


@router.post(
    "/projects/{project_id}/workflows/{workflow_id}/validate",
    response_model=list[StudioDiagnosticResponse],
)
def validate_studio_workflow(
    project_id: str,
    workflow_id: str,
) -> list[StudioDiagnosticResponse]:
    service = get_studio_project(project_id)

    for workflow in service.list_workflows():
        if workflow.id == workflow_id:
            definition = service.load_workflow(workflow.path)
            diagnostics = service.validate_workflow(definition)

            return [
                diagnostic_response(diagnostic)
                for diagnostic in diagnostics
            ]

    raise HTTPException(
        status_code=404,
        detail=f"Workflow '{workflow_id}' was not found.",
    )


@router.post(
    "/projects/{project_id}/workflows/{workflow_id}/run",
    response_model=StudioWorkflowRunResponse,
)
def run_studio_workflow(
    project_id: str,
    workflow_id: str,
    request: StudioWorkflowRunRequest,
) -> StudioWorkflowRunResponse:
    service = get_studio_project(project_id)

    workflow_path: Path | None = None

    for workflow in service.list_workflows():
        if workflow.id == workflow_id:
            workflow_path = workflow.path
            break

    if workflow_path is None:
        raise HTTPException(
            status_code=404,
            detail=f"Workflow '{workflow_id}' was not found.",
        )

    definition = service.load_workflow(workflow_path)

    diagnostics = service.validate_workflow(definition)

    errors = [
        diagnostic
        for diagnostic in diagnostics
        if diagnostic.severity.lower() == "error"
    ]

    if errors:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Workflow validation failed.",
                "diagnostics": [
                    diagnostic_response(
                        diagnostic
                    ).model_dump()
                    for diagnostic in errors
                ],
            },
        )

    runtime_workflow = service.get_runtime_workflow(
        definition.id,
    )

    existing_instance_ids: set[str] = set()

    if runtime_workflow is not None:
        existing_instance_ids = set(
            getattr(
                runtime_workflow.executor.store,
                "instances",
                {},
            ).keys()
        )

    try:
        result = service.execute_runtime_workflow(
            definition,
            variables=request.variables,
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    runtime_workflow = service.get_runtime_workflow(
        definition.id,
    )

    new_instance_ids: set[str] | None = None

    if runtime_workflow is not None:
        current_instance_ids = set(
            getattr(
                runtime_workflow.executor.store,
                "instances",
                {},
            ).keys()
        )

        new_instance_ids = (
            current_instance_ids - existing_instance_ids
        )

    return studio_run_response(
        service,
        definition.id,
        result,
        instance_ids=new_instance_ids,
    )


@router.post(
    "/projects/{project_id}/workflows/{workflow_id}/instances/{instance_id}/human-task",
    response_model=StudioWorkflowRunResponse,
)
def resolve_studio_human_task(
    project_id: str,
    workflow_id: str,
    instance_id: str,
    request: StudioWorkflowHumanTaskRequest,
) -> StudioWorkflowRunResponse:
    service = get_studio_project(project_id)

    action = request.action.strip().lower()

    if action not in {"approved", "rejected"}:
        raise HTTPException(
            status_code=400,
            detail=(
                "Human task action must be 'approved' or 'rejected'."
            ),
        )

    try:
        result = service.resume_runtime_workflow(
            workflow_id,
            instance_id,
            action,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return studio_run_response(
        service,
        workflow_id,
        result,
        instance_ids={instance_id},
    )

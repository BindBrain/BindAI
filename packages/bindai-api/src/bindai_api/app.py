from __future__ import annotations

from bindai_automation import AutomationDefinition, AutomationWorker
from bindai_project import Project
from fastapi import FastAPI

from .models import HealthResponse
from .routes.agents import router as agents_router
from .routes.projects import router as projects_router
from .routes.runs import router as runs_router
from .routes.workflows import router as workflows_router

app = FastAPI(
    title="BindAI API",
    version="0.1.0",
    description="REST API for the BindAI Framework.",
)

_application = None
_projects: dict[str, Project] = {}
_automations: dict[str, AutomationDefinition] = {}
_automation_worker = AutomationWorker()


def configure_application(application) -> None:
    """Configure the BindAI Application served by this API."""
    global _application
    _application = application


def get_configured_application():
    """Return the configured BindAI Application."""
    if _application is None:
        raise RuntimeError(
            "No BindAI application has been configured. "
            "Call configure_application() before serving requests."
        )

    return _application


def configure_project(project: Project) -> None:
    """Register a BindAI Project with the API."""
    _projects[project.name] = project


def get_configured_projects() -> list[Project]:
    """Return all projects registered with the API."""
    return list(_projects.values())


def get_configured_project(name: str) -> Project | None:
    """Return a registered project by name."""
    return _projects.get(name)


def configure_automation(
    automation: AutomationDefinition,
) -> None:
    """Register an AutomationDefinition with the API."""
    _automations[automation.id] = automation


def get_configured_automations() -> list[AutomationDefinition]:
    """Return all automations registered with the API."""
    return list(_automations.values())


def get_configured_automation(
    automation_id: str,
) -> AutomationDefinition | None:
    """Return a registered automation by ID."""
    return _automations.get(automation_id)


def get_automation_worker() -> AutomationWorker:
    """Return the shared automation worker used by the API."""
    return _automation_worker


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="bindai-api",
    )


app.include_router(agents_router)
app.include_router(workflows_router)
app.include_router(projects_router)
app.include_router(runs_router)

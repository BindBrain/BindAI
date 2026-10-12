from __future__ import annotations

import os
from pathlib import Path

from bindai_automation import AutomationDefinition, AutomationWorker
from bindai_project import Project
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .models import HealthResponse
from .routes.agents import router as agents_router
from .routes.projects import router as projects_router
from .routes.runs import router as runs_router
from .routes.studio import (
    configure_studio_workspace,
)
from .routes.studio import (
    router as studio_router,
)
from .routes.workflows import router as workflows_router

load_dotenv(
    Path(__file__).resolve().parents[4] / ".env",
)


app = FastAPI(
    title="BindAI API",
    version="0.1.1",
    description="REST API for the BindAI Framework.",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


_application = None
_projects: dict[str, Project] = {}
_automations: dict[str, AutomationDefinition] = {}
_automation_worker = AutomationWorker()


def _configure_studio() -> None:
    """
    Configure Studio from the BindAI Studio workspace environment variable.

    The workspace contains one or more directories with bindai.toml files.
    """
    workspace_value = os.getenv("BINDAI_STUDIO_WORKSPACE")

    if not workspace_value:
        raise RuntimeError("BINDAI_STUDIO_WORKSPACE is not configured.")

    workspace_root = Path(workspace_value).expanduser().resolve()

    if not workspace_root.is_dir():
        raise RuntimeError(f"BINDAI_STUDIO_WORKSPACE does not exist: {workspace_root}")

    configure_studio_workspace(workspace_root)


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
app.include_router(studio_router)


studio_directory = Path(__file__).parent / "studio" / "dist"

app.mount(
    "/studio",
    StaticFiles(
        directory=studio_directory,
        html=True,
    ),
    name="studio",
)

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..auth import require_api_key

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["projects"],
    dependencies=[Depends(require_api_key)],
)


@router.get("")
def list_projects() -> list[dict[str, str]]:
    from ..app import get_configured_projects

    return [
        {
            "name": project.name,
        }
        for project in get_configured_projects()
    ]


@router.get("/{project_name}")
def get_project(project_name: str) -> dict[str, str]:
    from ..app import get_configured_project

    project = get_configured_project(project_name)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project '{project_name}' was not found.",
        )

    return {
        "name": project.name,
    }

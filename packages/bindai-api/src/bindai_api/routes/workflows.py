from __future__ import annotations

from bindai_core.context import ExecutionContext
from bindai_workflow import WorkflowRegistry
from fastapi import APIRouter, Depends, HTTPException

from ..auth import require_api_key
from ..models import WorkflowRunRequest, WorkflowRunResponse

router = APIRouter(
    prefix="/api/v1/workflows",
    tags=["workflows"],
    dependencies=[Depends(require_api_key)],
)


@router.get("")
def list_workflows() -> list[dict[str, str]]:
    return [
        {
            "id": workflow.id,
            "name": workflow.name,
        }
        for workflow in WorkflowRegistry.all()
    ]


@router.post(
    "/{workflow_id}/run",
    response_model=WorkflowRunResponse,
)
def run_workflow(
    workflow_id: str,
    request: WorkflowRunRequest,
) -> WorkflowRunResponse:
    try:
        workflow = WorkflowRegistry.get(workflow_id)
    except KeyError:
        workflow = None

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail=f"Workflow '{workflow_id}' was not found.",
        )

    context = ExecutionContext()
    context.variables.update(request.variables)

    result = workflow.run(context)

    return WorkflowRunResponse(
        workflow=workflow.id,
        result=result,
    )

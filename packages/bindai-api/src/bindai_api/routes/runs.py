from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..auth import require_api_key
from ..models import (
    AutomationRunRequest,
    AutomationRunResponse,
)

router = APIRouter(
    prefix="/api/v1/runs",
    tags=["runs"],
    dependencies=[Depends(require_api_key)],
)


def _to_response(run) -> AutomationRunResponse:
    return AutomationRunResponse(
        id=run.id,
        definition_id=run.definition_id,
        definition_version=run.definition_version,
        status=run.status,
        input=run.input,
        output=run.output,
        error=run.error,
        created_at=run.created_at,
        started_at=run.started_at,
        completed_at=run.completed_at,
    )


@router.post(
    "",
    response_model=AutomationRunResponse,
    status_code=202,
)
def create_run(
    request: AutomationRunRequest,
) -> AutomationRunResponse:
    from ..app import (
        get_automation_worker,
        get_configured_automation,
    )

    automation = get_configured_automation(request.automation_id)

    if automation is None:
        raise HTTPException(
            status_code=404,
            detail=(f"Automation '{request.automation_id}' was not found."),
        )

    worker = get_automation_worker()

    run, _ = worker.submit_with_run(
        automation,
        input=request.input,
    )

    return _to_response(run)


@router.get(
    "/{run_id}",
    response_model=AutomationRunResponse,
)
def get_run(run_id: str) -> AutomationRunResponse:
    from ..app import get_automation_worker

    worker = get_automation_worker()

    run = worker.state_store.load(run_id)

    if run is None:
        run = worker.history.get(run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail=f"Run '{run_id}' was not found.",
        )

    return _to_response(run)

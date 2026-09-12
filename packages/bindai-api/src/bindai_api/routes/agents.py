from __future__ import annotations

from collections.abc import Iterator

from bindai.application import Application
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from ..auth import require_api_key
from ..dependencies import get_application
from ..models import AgentRunRequest, AgentRunResponse

router = APIRouter(
    prefix="/api/v1/agents",
    tags=["agents"],
    dependencies=[Depends(require_api_key)],
)


def _find_agent(
    application: Application,
    agent_name: str,
):
    agents = application.agents.all()

    return next(
        (registered_agent for registered_agent in agents if registered_agent.name == agent_name),
        None,
    )


@router.get("")
def list_agents(
    application: Application = Depends(get_application),
) -> list[dict[str, str]]:
    return [
        {
            "name": agent.name,
        }
        for agent in application.agents.all()
    ]


@router.post(
    "/{agent_name}/run",
    response_model=AgentRunResponse,
)
def run_agent(
    agent_name: str,
    request: AgentRunRequest,
    application: Application = Depends(get_application),
) -> AgentRunResponse:
    agent = _find_agent(
        application,
        agent_name,
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_name}' was not found.",
        )

    response = agent.chat(request.message)

    return AgentRunResponse(
        agent=agent_name,
        response=response,
    )


@router.post(
    "/{agent_name}/stream",
)
def stream_agent(
    agent_name: str,
    request: AgentRunRequest,
    application: Application = Depends(get_application),
) -> StreamingResponse:
    agent = _find_agent(
        application,
        agent_name,
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_name}' was not found.",
        )

    stream = agent.stream_chat(request.message)

    def generate() -> Iterator[str]:
        for chunk in stream:
            if isinstance(chunk, str):
                yield chunk
            else:
                yield str(chunk)

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )

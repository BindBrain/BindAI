from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    message: str = Field(min_length=1)


class AgentRunResponse(BaseModel):
    agent: str
    response: Any


class WorkflowRunRequest(BaseModel):
    variables: dict[str, Any] = Field(default_factory=dict)


class WorkflowRunResponse(BaseModel):
    workflow: str
    result: Any


class AutomationRunRequest(BaseModel):
    automation_id: str = Field(min_length=1)
    input: Any = None


class AutomationRunResponse(BaseModel):
    id: str
    definition_id: str
    definition_version: int
    status: str
    input: Any = None
    output: Any = None
    error: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None


class HealthResponse(BaseModel):
    status: str
    service: str

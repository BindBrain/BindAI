from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StudioProjectResponse(BaseModel):
    name: str
    path: str
    workflow_count: int
    agent_count: int
    form_count: int


class StudioProjectCreateRequest(BaseModel):
    name: str


class StudioProjectCreateResponse(BaseModel):
    name: str
    path: str
    workflow_count: int
    agent_count: int
    form_count: int


class StudioWorkflowResponse(BaseModel):
    id: str
    name: str
    path: str


class StudioWorkflowCreateRequest(BaseModel):
    name: str
    id: str | None = None


class StudioWorkflowCreateResponse(BaseModel):
    workflow: dict[str, Any]
    path: str
    diagnostics: list["StudioDiagnosticResponse"] = Field(
        default_factory=list
    )


class StudioDiagnosticResponse(BaseModel):
    severity: str
    code: str
    message: str
    node_id: str | None = None
    node_type: str | None = None
    suggestion: str | None = None


class StudioWorkflowNodeRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    type: str
    name: str | None = None
    configuration: dict[str, Any] = Field(
        default_factory=dict
    )

    def to_definition_dict(self) -> dict[str, Any]:
        data = {
            "id": self.id,
            "type": self.type,
        }

        if self.name is not None:
            data["name"] = self.name

        data.update(self.configuration)

        for key, value in self.model_extra.items():
            if key not in {
                "id",
                "type",
                "name",
                "configuration",
            }:
                data[key] = value

        return data


class StudioWorkflowEdgeRequest(BaseModel):
    source: str = Field(alias="from")
    target: str = Field(alias="to")
    port: str | None = None

    model_config = {
        "populate_by_name": True,
    }

    def to_definition_dict(self) -> dict[str, Any]:
        data = {
            "from": self.source,
            "to": self.target,
        }

        if self.port is not None:
            data["port"] = self.port

        return data


class StudioWorkflowPayload(BaseModel):
    id: str
    name: str
    nodes: list[StudioWorkflowNodeRequest] = Field(
        default_factory=list
    )
    edges: list[StudioWorkflowEdgeRequest] = Field(
        default_factory=list
    )

    def to_definition_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "nodes": [
                node.to_definition_dict()
                for node in self.nodes
            ],
            "edges": [
                edge.to_definition_dict()
                for edge in self.edges
            ],
        }


class StudioWorkflowDefinitionRequest(BaseModel):
    version: int = 1
    workflow: StudioWorkflowPayload

    def to_definition_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "workflow": self.workflow.to_definition_dict(),
        }


class StudioWorkflowSaveResponse(BaseModel):
    workflow: dict[str, Any]
    diagnostics: list[StudioDiagnosticResponse]


class StudioWorkflowRunRequest(BaseModel):
    variables: dict[str, Any] = Field(
        default_factory=dict
    )


class StudioHumanTaskResponse(BaseModel):
    id: str
    node_id: str
    assignee: str | None = None
    role: str | None = None
    completed: bool = False
    result: str | None = None
    created_at: str


class StudioWorkflowRunResponse(BaseModel):
    workflow: str
    instance_id: str | None = None
    waiting: bool = False
    human_task: StudioHumanTaskResponse | None = None
    result: Any


class StudioWorkflowHumanTaskRequest(BaseModel):
    action: str


class StudioAgentResponse(BaseModel):
    id: str
    name: str
    path: str

class StudioKnowledgeResponse(BaseModel):
    id: str
    name: str
    path: str
    type: str


class StudioToolResponse(BaseModel):
    id: str
    name: str
    description: str
    parameters: dict[str, Any] = Field(
        default_factory=dict,
    )


class StudioAgentCreateRequest(BaseModel):
    name: str
    id: str | None = None


class StudioAgentCreateResponse(BaseModel):
    agent: dict[str, Any]
    path: str


class StudioAgentDefinitionResponse(BaseModel):
    agent: dict[str, Any]


class StudioAgentDefinitionRequest(BaseModel):
    agent: dict[str, Any]


class StudioFormResponse(BaseModel):
    id: str
    name: str
    path: str


class StudioFormCreateRequest(BaseModel):
    name: str
    id: str | None = None


class StudioFormCreateResponse(BaseModel):
    form: dict[str, Any]
    path: str


class StudioFormDefinitionResponse(BaseModel):
    form: dict[str, Any]


class StudioFormDefinitionRequest(BaseModel):
    form: dict[str, Any]



class StudioConnectionResponse(BaseModel):
    name: str
    provider: str
    configured: bool


class StudioConnectionCreateRequest(BaseModel):
    name: str
    provider: str


class StudioConnectionCredentialRequest(BaseModel):
    credential: str

from __future__ import annotations

from pathlib import Path

import pytest

from bindai_agent import AgentDefinition, AgentRegistry
from bindai_project import (
    ProjectStudioService,
    ProjectSummary,
)
from bindai_workflow import (
    WorkflowDefinition,
    WorkflowEdgeDefinition,
    WorkflowNodeDefinition,
)


def create_project(root: Path) -> Path:
    root.mkdir()

    (root / "bindai.toml").write_text(
        'name = "Studio Test"\nworkflows = "workflows"\nagents = "agents"\n',
        encoding="utf-8",
    )

    (root / "workflows").mkdir()
    (root / "agents").mkdir()

    return root


def create_workflow() -> WorkflowDefinition:
    return WorkflowDefinition(
        id="hello",
        name="Hello Workflow",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="end",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="end",
            ),
        ],
    )


def test_service_requires_bindai_project(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Not a BindAI project"):
        ProjectStudioService(tmp_path)


def test_summary(tmp_path: Path) -> None:
    root = create_project(tmp_path / "project")

    service = ProjectStudioService(root)

    summary = service.summary()

    assert isinstance(summary, ProjectSummary)
    assert summary.name == "Studio Test"
    assert summary.path == root.resolve()
    assert summary.workflow_count == 0


def test_discover_projects(tmp_path: Path) -> None:
    first = create_project(tmp_path / "first")
    second = create_project(tmp_path / "second")

    (first / "bindai.toml").write_text(
        'name = "First"\n',
        encoding="utf-8",
    )
    (second / "bindai.toml").write_text(
        'name = "Second"\n',
        encoding="utf-8",
    )

    projects = ProjectStudioService.discover_projects(tmp_path)

    assert [project.name for project in projects] == [
        "First",
        "Second",
    ]


def test_save_and_load_workflow(tmp_path: Path) -> None:
    root = create_project(tmp_path / "project")
    service = ProjectStudioService(root)

    workflow = create_workflow()

    path = service.save_workflow(workflow)

    assert path == (
        root / "workflows" / "hello.yaml"
    )

    loaded = service.load_workflow(path)

    assert loaded.id == "hello"
    assert loaded.name == "Hello Workflow"
    assert len(loaded.nodes) == 2
    assert len(loaded.edges) == 1


def test_list_workflows(tmp_path: Path) -> None:
    root = create_project(tmp_path / "project")
    service = ProjectStudioService(root)

    service.save_workflow(create_workflow())

    workflows = service.list_workflows()

    assert len(workflows) == 1
    assert workflows[0].id == "hello"
    assert workflows[0].name == "Hello Workflow"


def test_validate_workflow(tmp_path: Path) -> None:
    root = create_project(tmp_path / "project")
    service = ProjectStudioService(root)

    workflow = WorkflowDefinition(
        id="broken",
        name="Broken Workflow",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="missing",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="does-not-exist",
            ),
        ],
    )

    diagnostics = service.validate_workflow(workflow)

    assert diagnostics
    assert any(
        diagnostic.code == "workflow.invalid_node_reference"
        for diagnostic in diagnostics
    )


def test_build_runtime_workflow_loads_studio_agent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = create_project(tmp_path / "project")
    service = ProjectStudioService(root)

    agent_definition = AgentDefinition(
        id="support-agent",
        name="Support Agent",
    )

    service.save_agent(agent_definition)

    class FakeAgent:
        name = "Support Agent"

    def fake_build_agent(
        definition: AgentDefinition,
        *,
        project_root: Path,
        memory=None,
        retriever=None,
        knowledge=None,
    ) -> FakeAgent:
        assert definition.id == "support-agent"
        assert definition.name == "Support Agent"
        assert project_root == root.resolve()

        agent = FakeAgent()
        AgentRegistry.register(agent)
        AgentRegistry.register_alias(
            definition.id,
            agent,
        )
        return agent

    monkeypatch.setattr(
        "bindai_project.studio.build_agent",
        fake_build_agent,
    )
    AgentRegistry.clear()

    workflow = WorkflowDefinition(
        id="agent-workflow",
        name="Agent Workflow",
        nodes=[
            WorkflowNodeDefinition(
                id="start",
                type="start",
            ),
            WorkflowNodeDefinition(
                id="agent",
                type="agent",
                configuration={
                    "agent": "support-agent",
                    "input_variable": "input",
                    "output_variable": "output",
                },
            ),
            WorkflowNodeDefinition(
                id="end",
                type="end",
            ),
        ],
        edges=[
            WorkflowEdgeDefinition(
                source="start",
                target="agent",
            ),
            WorkflowEdgeDefinition(
                source="agent",
                target="end",
            ),
        ],
    )

    executable = service.build_runtime_workflow(
        workflow,
        clear_registry=True,
    )

    assert executable.id == "agent-workflow"
    assert executable.start_node == "start"
    assert "agent" in executable.nodes
    assert executable.nodes["agent"].agent == "support-agent"
    assert AgentRegistry.contains("support-agent")

    AgentRegistry.clear()

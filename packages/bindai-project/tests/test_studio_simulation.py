from pathlib import Path

from bindai_project import ProjectCreator
from bindai_project.studio import ProjectStudioService
from bindai_tool import FunctionTool, ToolRegistry
from bindai_workflow import (
    EndNode,
    StartNode,
    ToolNode,
    Workflow,
    WorkflowDefinition,
)


def test_simulate_runtime_workflow_blocks_tool_side_effect(
    tmp_path: Path,
    monkeypatch,
):
    project_root = tmp_path / "demo"

    ProjectCreator().create(
        project_root,
        project_name="demo",
    )

    service = ProjectStudioService(
        project_root,
    )

    calls: list[str] = []

    def dangerous_tool():
        calls.append("executed")
        return "REAL SIDE EFFECT"

    registry = ToolRegistry()

    registry.register(
        FunctionTool(
            function=dangerous_tool,
            name="dangerous_tool",
        )
    )

    runtime_workflow = Workflow(
        name="Simulation Test",
    )

    runtime_workflow.add_node(
        StartNode(
            "start",
        )
    )

    runtime_workflow.add_node(
        ToolNode(
            node_id="tool",
            tool=registry.get(
                "dangerous_tool",
            ),
        )
    )

    runtime_workflow.add_node(
        EndNode(
            "end",
        )
    )

    runtime_workflow.nodes["start"].next_nodes = [
        "tool",
    ]

    runtime_workflow.nodes["tool"].next_nodes = [
        "end",
    ]

    monkeypatch.setattr(
        service,
        "build_runtime_workflow",
        lambda workflow, load_agents=True, clear_registry=False: (
            runtime_workflow
        ),
    )

    definition = WorkflowDefinition(
        id="simulation-test",
        name="Simulation Test",
    )

    result = service.simulate_runtime_workflow(
        definition,
    )

    assert result.success is True

    assert calls == []

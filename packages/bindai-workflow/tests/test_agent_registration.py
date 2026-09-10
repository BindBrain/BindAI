from bindai_agent.registry import AgentRegistry
from bindai_workflow import WorkflowBuilder


class DummyAgent:
    name = "test-agent"


def test_agent_is_registered_when_added_to_workflow():
    AgentRegistry.clear()

    agent = DummyAgent()

    workflow = WorkflowBuilder("test-workflow").start_node().agent(agent).end_node().build()

    assert AgentRegistry.contains("test-agent")
    assert workflow.name == "test-workflow"
    assert "test-agent" in workflow.nodes

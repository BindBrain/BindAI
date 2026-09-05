from bindai_agent import AgentDelegationTool
from bindai_agent.result import AgentResult


class FakeAgent:
    name = "Researcher"

    def __init__(self):
        self.received_message = None

    def run(self, message):
        self.received_message = message
        return AgentResult(success=True, output="Research completed.")


def test_agent_delegation_tool():
    agent = FakeAgent()
    tool = AgentDelegationTool(agent)

    context = type("Context", (), {})()
    context.variables = {"message": "Find information about AI agents."}

    result = tool.execute(context)

    assert result.success is True
    assert result.value == "Research completed."
    assert agent.received_message == "Find information about AI agents."

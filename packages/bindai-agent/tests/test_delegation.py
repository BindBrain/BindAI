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

def test_agent_team_delegation_tool():
    from bindai_agent import AgentResult, AgentTeam

    class TeamAgent:
        def __init__(self, name, output):
            self.name = name
            self.output = output
            self.received_message = None

        def run(self, message):
            self.received_message = message
            return AgentResult(
                success=True,
                output=self.output,
            )

    researcher = TeamAgent("Researcher", "Research completed.")
    writer = TeamAgent("Writer", "Writing completed.")

    team = AgentTeam(name="Content Team")
    team.add(researcher).add(writer)

    from bindai_agent import AgentTeamDelegationTool

    tool = AgentTeamDelegationTool(team)

    context = type("Context", (), {})()
    context.variables = {
        "message": "Create an article about AI agents."
    }

    result = tool.execute(context)

    assert result.success is True
    assert result.value == {
        "Researcher": "Research completed.",
        "Writer": "Writing completed.",
    }

    assert researcher.received_message == "Create an article about AI agents."
    assert writer.received_message == "Create an article about AI agents."

def test_agent_team_delegation_tool_propagates_failure():
    from bindai_agent import AgentResult, AgentTeam, AgentTeamDelegationTool

    class FailingAgent:
        name = "Researcher"

        def run(self, message):
            return AgentResult(
                success=False,
                error="Research failed.",
            )

    team = AgentTeam(name="Research Team")
    team.add(FailingAgent())

    tool = AgentTeamDelegationTool(team)

    context = type("Context", (), {})()
    context.variables = {
        "message": "Research AI agents."
    }

    result = tool.execute(context)

    assert result.success is False
    assert result.error == "Research failed."

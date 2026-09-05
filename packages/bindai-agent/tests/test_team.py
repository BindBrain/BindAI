from bindai_agent import AgentTeam


class FakeAgent:
    def __init__(self, name):
        self.name = name


def test_agent_team_manages_agents():
    team = AgentTeam(name="Research Team")

    researcher = FakeAgent("Researcher")
    writer = FakeAgent("Writer")

    team.add(researcher)
    team.add(writer)

    assert team.name == "Research Team"
    assert team.size() == 2
    assert team.names() == ["Researcher", "Writer"]
    assert team.get("Researcher") is researcher
    assert team.contains("Writer") is True

    team.remove("Writer")

    assert team.size() == 1
    assert team.contains("Writer") is False

def test_agent_team_with_real_agents():
    from bindai_agent import AgentBuilder

    researcher = AgentBuilder().name("Researcher").build()
    writer = AgentBuilder().name("Writer").build()

    team = AgentTeam(name="Content Team")
    team.add(researcher).add(writer)

    assert team.size() == 2
    assert team.get("Researcher") is researcher
    assert team.get("Writer") is writer
def test_agent_team_runs_agents_sequentially():
    class FakeAgent:
        def __init__(self, name, output):
            self.name = name
            self.output = output
            self.received_message = None

        def run(self, message):
            from bindai_agent import AgentResult

            self.received_message = message

            return AgentResult(
                success=True,
                output=self.output,
            )

    first = FakeAgent("Researcher", "Research complete.")
    second = FakeAgent("Writer", "Draft complete.")

    team = AgentTeam(name="Content Team")
    team.add(first).add(second)

    result = team.run("Create an article about AI agents.")

    assert result.success is True
    assert result.output == {
        "Researcher": "Research complete.",
        "Writer": "Draft complete.",
    }
    assert first.received_message == "Create an article about AI agents."
    assert second.received_message == "Create an article about AI agents."

def test_agent_team_stops_when_agent_fails():
    class FakeAgent:
        def __init__(self, name, result):
            self.name = name
            self.result = result

        def run(self, message):
            return self.result

    from bindai_agent import AgentResult

    first = FakeAgent(
        "Researcher",
        AgentResult(success=True, output="Research complete."),
    )
    second = FakeAgent(
        "Writer",
        AgentResult(success=False, error="Writer failed."),
    )

    team = AgentTeam(name="Content Team")
    team.add(first).add(second)

    result = team.run("Create an article.")

    assert result.success is False
    assert result.output == {
        "Researcher": "Research complete.",
    }
    assert result.error == "Writer failed."

def test_agent_team_runs_agents_in_parallel():
    import time

    from bindai_agent import AgentResult

    class SlowAgent:
        def __init__(self, name, output):
            self.name = name
            self.output = output

        def run(self, message):
            time.sleep(0.2)
            return AgentResult(
                success=True,
                output=self.output,
            )

    first = SlowAgent("Researcher", "Research complete.")
    second = SlowAgent("Writer", "Draft complete.")

    team = AgentTeam(name="Content Team")
    team.add(first).add(second)

    start = time.perf_counter()

    result = team.run_parallel("Create an article.")

    elapsed = time.perf_counter() - start

    assert result.success is True
    assert result.output == {
        "Researcher": "Research complete.",
        "Writer": "Draft complete.",
    }
    assert elapsed < 0.35

def test_agent_team_chains_agent_outputs():
    from bindai_agent import AgentResult

    class ChainAgent:
        def __init__(self, name, suffix):
            self.name = name
            self.suffix = suffix
            self.received_message = None

        def run(self, message):
            self.received_message = message

            return AgentResult(
                success=True,
                output=f"{message} -> {self.suffix}",
            )

    first = ChainAgent("Researcher", "research")
    second = ChainAgent("Writer", "draft")
    third = ChainAgent("Reviewer", "review")

    team = AgentTeam(name="Content Team")
    team.add(first).add(second).add(third)

    result = team.run_chain("Create an article about AI agents.")

    assert result.success is True
    assert result.output == "Create an article about AI agents. -> research -> draft -> review"

    assert first.received_message == "Create an article about AI agents."
    assert second.received_message == "Create an article about AI agents. -> research"
    assert third.received_message == "Create an article about AI agents. -> research -> draft"

def test_agent_team_parallel_then_review():
    from bindai_agent import AgentResult

    class TeamAgent:
        def __init__(self, name, output):
            self.name = name
            self.output = output
            self.received_message = None

        def run(self, message):
            self.received_message = message
            return AgentResult(success=True, output=self.output)

    researcher = TeamAgent("Researcher", "Research findings")
    writer = TeamAgent("Writer", "Draft content")
    reviewer = TeamAgent("Reviewer", "Final reviewed result")

    team = AgentTeam(name="Content Team")
    team.add(researcher).add(writer).add(reviewer)

    result = team.run_parallel_then_review(
        "Create an article about AI agents."
    )

    assert result.success is True
    assert result.output == "Final reviewed result"
    assert reviewer.received_message == (
        "Researcher: Research findings\n"
        "Writer: Draft content"
    )

def test_agent_team_supports_agent_roles():
    class RoleAgent:
        def __init__(self, name):
            self.name = name

    researcher = RoleAgent("Researcher")
    writer = RoleAgent("Writer")

    team = AgentTeam(name="Content Team")
    team.add(researcher, role="research")
    team.add(writer, role="writing")

    assert team.role("research") is researcher
    assert team.role("writing") is writer
    assert team.roles() == ["research", "writing"]

def test_agent_team_runs_agent_by_role():
    from bindai_agent import AgentResult

    class RoleAgent:
        def __init__(self, name):
            self.name = name
            self.received_message = None

        def run(self, message):
            self.received_message = message
            return AgentResult(
                success=True,
                output=f"{self.name}: {message}",
            )

    researcher = RoleAgent("Researcher")
    writer = RoleAgent("Writer")

    team = AgentTeam(name="Content Team")
    team.add(researcher, role="research")
    team.add(writer, role="writing")

    result = team.run_role("research", "Research AI agents.")

    assert result.success is True
    assert result.output == "Researcher: Research AI agents."
    assert researcher.received_message == "Research AI agents."
    assert writer.received_message is None
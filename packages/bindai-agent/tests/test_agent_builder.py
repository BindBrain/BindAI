from bindai_agent import Agent, AssistantAgent


def test_agent_builder_returns_assistant_agent():
    agent = Agent.builder().name("test-agent").instructions("You are a test assistant.").build()

    assert isinstance(agent, AssistantAgent)
    assert agent.name == "test-agent"
    assert agent.instructions == "You are a test assistant."

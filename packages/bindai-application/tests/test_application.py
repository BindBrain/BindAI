from bindai_application import Application, ApplicationConfiguration


class FakeAgent:
    def __init__(self, name: str):
        self.name = name
        self.chat_messages: list[str] = []
        self.stream_messages: list[str] = []

    def chat(self, message: str):
        self.chat_messages.append(message)
        return f"chat:{message}"

    def stream_chat(self, message: str):
        self.stream_messages.append(message)
        return f"stream:{message}"


def make_application(
    name: str = "test-app",
    description: str = "",
) -> Application:
    return Application(
        ApplicationConfiguration(
            name=name,
            description=description,
        )
    )


def test_configuration_defaults():
    configuration = ApplicationConfiguration(
        name="test-app",
    )

    assert configuration.name == "test-app"
    assert configuration.description == ""


def test_application_initializes_with_empty_resources():
    application = make_application(
        description="Test application",
    )

    assert application.name == "test-app"
    assert application.configuration.description == "Test application"
    assert application.agents == {}
    assert application.workflows == {}
    assert application.knowledge == {}
    assert application.memories == {}
    assert len(application) == 0


def test_add_agent_registers_and_returns_application():
    application = make_application()
    agent = FakeAgent("assistant")

    result = application.add_agent(agent)

    assert result is application
    assert application.agent("assistant") is agent
    assert "assistant" in application
    assert len(application) == 1
    assert list(application) == [agent]


def test_add_agent_replaces_agent_with_same_name():
    application = make_application()
    first = FakeAgent("assistant")
    second = FakeAgent("assistant")

    application.add_agent(first)
    application.add_agent(second)

    assert len(application) == 1
    assert application.agent("assistant") is second


def test_agent_raises_key_error_for_unknown_agent():
    application = make_application()

    try:
        application.agent("missing")
    except KeyError as error:
        assert error.args == ("missing",)
    else:
        raise AssertionError("Expected KeyError")


def test_run_delegates_to_agent_chat():
    application = make_application()
    agent = FakeAgent("assistant")
    application.add_agent(agent)

    result = application.run(
        agent="assistant",
        message="Hello",
    )

    assert result == "chat:Hello"
    assert agent.chat_messages == ["Hello"]


def test_stream_delegates_to_agent_stream_chat():
    application = make_application()
    agent = FakeAgent("assistant")
    application.add_agent(agent)

    result = application.stream(
        agent="assistant",
        message="Hello",
    )

    assert result == "stream:Hello"
    assert agent.stream_messages == ["Hello"]


def test_iteration_returns_registered_agents():
    application = make_application()
    first = FakeAgent("first")
    second = FakeAgent("second")

    application.add_agent(first)
    application.add_agent(second)

    assert list(application) == [first, second]
    assert set(application.agents) == {"first", "second"}
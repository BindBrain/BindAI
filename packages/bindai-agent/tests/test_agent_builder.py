from bindai_agent import Agent, AssistantAgent


def test_agent_builder_returns_assistant_agent():
    agent = Agent.builder().name("test-agent").instructions("You are a test assistant.").build()

    assert isinstance(agent, AssistantAgent)
    assert agent.name == "test-agent"
    assert agent.instructions == "You are a test assistant."


def test_agent_builder_provider_name_uses_resolver(monkeypatch):
    sentinel = object()

    def fake_resolve_provider(provider, **kwargs):
        assert provider == "anthropic"
        assert kwargs == {
            "api_key": None,
            "endpoint": None,
            "organization": None,
            "model": None,
        }
        return sentinel

    monkeypatch.setattr(
        "bindai_agent.builder.resolve_provider",
        fake_resolve_provider,
    )

    agent = Agent.builder().provider("anthropic").build()

    assert agent.provider is sentinel


def test_agent_builder_provider_instance_is_preserved():
    provider = object()

    agent = Agent.builder().provider(provider).build()

    assert agent.provider is provider


def test_agent_builder_provider_forwards_configuration(monkeypatch):
    captured = {}

    def fake_resolve_provider(provider, **kwargs):
        captured["provider"] = provider
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(
        "bindai_agent.builder.resolve_provider",
        fake_resolve_provider,
    )

    agent = (
        Agent.builder()
        .provider(
            "anthropic",
            api_key="test-key",
            endpoint="https://example.com",
            organization="test-org",
            model="claude-test",
        )
        .build()
    )

    assert agent.provider is not None
    assert captured["provider"] == "anthropic"
    assert captured["kwargs"] == {
        "api_key": "test-key",
        "endpoint": "https://example.com",
        "organization": "test-org",
        "model": "claude-test",
    }


def test_agent_builder_model_forwards_model_to_resolver(monkeypatch):
    captured = {}

    def fake_resolve_provider(provider, **kwargs):
        captured["provider"] = provider
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(
        "bindai_agent.builder.resolve_provider",
        fake_resolve_provider,
    )

    agent = Agent.builder().model("anthropic:claude-test").build()

    assert agent.provider is not None
    assert captured["provider"] == "anthropic"
    assert captured["kwargs"]["model"] == "claude-test"


def test_agent_builder_openai_forwards_model_to_resolver(monkeypatch):
    captured = {}

    def fake_resolve_provider(provider, **kwargs):
        captured["provider"] = provider
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(
        "bindai_agent.builder.resolve_provider",
        fake_resolve_provider,
    )

    agent = Agent.builder().openai("gpt-test").build()

    assert agent.provider is not None
    assert captured["provider"] == "openai"
    assert captured["kwargs"] == {
        "api_key": None,
        "endpoint": None,
        "organization": None,
        "model": "gpt-test",
    }

from bindai_config import (
    ApplicationAgentConfig,
    ApplicationConfig,
    ModelConfig,
)


def test_model_config_defaults() -> None:
    config = ModelConfig()

    assert config.provider == "openai"
    assert config.model == "gpt-4.1-mini"
    assert config.temperature == 0.7
    assert config.max_tokens is None


def test_model_config_accepts_custom_values() -> None:
    config = ModelConfig(
        provider="anthropic",
        model="claude-sonnet",
        temperature=0.2,
        max_tokens=4096,
    )

    assert config.provider == "anthropic"
    assert config.model == "claude-sonnet"
    assert config.temperature == 0.2
    assert config.max_tokens == 4096


def test_application_agent_config_defaults() -> None:
    config = ApplicationAgentConfig(
        name="Support Agent",
    )

    assert config.name == "Support Agent"
    assert config.instructions == ""
    assert config.model is None


def test_application_agent_config_accepts_model() -> None:
    model = ModelConfig(
        provider="openai",
        model="gpt-5",
        temperature=0.2,
    )

    config = ApplicationAgentConfig(
        name="Support Agent",
        instructions="Help customers.",
        model=model,
    )

    assert config.name == "Support Agent"
    assert config.instructions == "Help customers."
    assert config.model is model


def test_application_config_defaults() -> None:
    config = ApplicationConfig(
        name="customer-support",
    )

    assert config.name == "customer-support"
    assert config.description == ""
    assert config.type == "assistant"
    assert config.agent is None


def test_application_config_accepts_agent() -> None:
    config = ApplicationConfig(
        name="customer-support",
        description="Customer support assistant",
        type="assistant",
        agent=ApplicationAgentConfig(
            name="Support Agent",
            instructions="Help customers.",
            model=ModelConfig(
                provider="openai",
                model="gpt-5",
                temperature=0.2,
            ),
        ),
    )

    assert config.name == "customer-support"
    assert config.description == "Customer support assistant"
    assert config.type == "assistant"
    assert config.agent is not None
    assert config.agent.name == "Support Agent"
    assert config.agent.instructions == "Help customers."
    assert config.agent.model is not None
    assert config.agent.model.provider == "openai"
    assert config.agent.model.model == "gpt-5"
    assert config.agent.model.temperature == 0.2
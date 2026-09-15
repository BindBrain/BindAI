import pytest
from bindai_config import get_provider_connection, list_provider_connections


@pytest.mark.parametrize(
    (
        "provider",
        "api_key_env",
        "endpoint_env",
        "organization_env",
    ),
    [
        (
            "openai",
            "OPENAI_API_KEY",
            "OPENAI_BASE_URL",
            "OPENAI_ORGANIZATION",
        ),
        (
            "anthropic",
            "ANTHROPIC_API_KEY",
            None,
            None,
        ),
        (
            "google",
            "GEMINI_API_KEY",
            None,
            None,
        ),
        (
            "groq",
            "GROQ_API_KEY",
            None,
            None,
        ),
        (
            "ollama",
            None,
            "OLLAMA_HOST",
            None,
        ),
        (
            "openrouter",
            "OPENROUTER_API_KEY",
            None,
            None,
        ),
    ],
)
def test_get_provider_connection(
    provider,
    api_key_env,
    endpoint_env,
    organization_env,
):
    connection = get_provider_connection(provider)

    assert connection.provider == provider
    assert connection.api_key_env == api_key_env
    assert connection.endpoint_env == endpoint_env
    assert connection.organization_env == organization_env


def test_get_provider_connection_is_case_insensitive():
    connection = get_provider_connection("OpenAI")

    assert connection.provider == "openai"
    assert connection.api_key_env == "OPENAI_API_KEY"


def test_get_provider_connection_rejects_unknown_provider():
    with pytest.raises(
        KeyError,
        match='Unknown provider "unknown"',
    ):
        get_provider_connection("unknown")


def test_list_provider_connections_contains_known_providers():
    providers = {
        connection.provider
        for connection in list_provider_connections()
    }

    assert providers == {
        "openai",
        "anthropic",
        "google",
        "groq",
        "ollama",
        "openrouter",
    }


def test_provider_connection_is_immutable():
    connection = get_provider_connection("openai")

    with pytest.raises(AttributeError):
        connection.provider = "anthropic"

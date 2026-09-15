from pathlib import Path

from bindai_agent.provider_resolver import resolve_provider


def test_resolve_openai_uses_openai_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.com/v1")
    monkeypatch.setenv("OPENAI_ORGANIZATION", "org-123")

    captured = {}

    def fake_create(name, configuration=None, **kwargs):
        captured["name"] = name
        captured["configuration"] = configuration
        return object()

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ProviderRegistry.create",
        fake_create,
    )

    resolve_provider("openai")

    configuration = captured["configuration"]

    assert captured["name"] == "openai"
    assert configuration.api_key == "openai-key"
    assert configuration.endpoint == "https://example.com/v1"
    assert configuration.organization == "org-123"


def test_resolve_providers_use_provider_specific_api_keys(monkeypatch):
    environment = {
        "anthropic": ("ANTHROPIC_API_KEY", "anthropic-key"),
        "google": ("GEMINI_API_KEY", "google-key"),
        "groq": ("GROQ_API_KEY", "groq-key"),
        "openrouter": ("OPENROUTER_API_KEY", "openrouter-key"),
    }

    for provider, (environment_key, api_key) in environment.items():
        monkeypatch.setenv(environment_key, api_key)

        captured = {}

        def fake_create(name, configuration=None, **kwargs):
            captured["name"] = name
            captured["configuration"] = configuration
            return object()

        monkeypatch.setattr(
            "bindai_agent.provider_resolver.ProviderRegistry.create",
            fake_create,
        )

        resolve_provider(provider)

        assert captured["name"] == provider
        assert captured["configuration"].api_key == api_key


def test_resolve_ollama_uses_host_as_endpoint(monkeypatch):
    monkeypatch.setenv(
        "OLLAMA_HOST",
        "http://localhost:11434",
    )

    captured = {}

    def fake_create(name, configuration=None, **kwargs):
        captured["name"] = name
        captured["configuration"] = configuration
        return object()

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ProviderRegistry.create",
        fake_create,
    )

    resolve_provider("ollama")

    configuration = captured["configuration"]

    assert captured["name"] == "ollama"
    assert configuration.api_key is None
    assert configuration.endpoint == "http://localhost:11434"


def test_resolve_provider_uses_project_model_and_timeout(monkeypatch):
    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ProjectRuntime",
        lambda *root: type(
            "Runtime",
            (),
            {
                "config": type(
                    "Config",
                    (),
                    {
                        "model": "test-model",
                        "timeout": 42,
                    },
                )()
            },
        )(),
    )

    captured = {}

    def fake_create(name, configuration=None, **kwargs):
        captured["configuration"] = configuration
        return object()

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ProviderRegistry.create",
        fake_create,
    )

    resolve_provider("openai")

    configuration = captured["configuration"]

    assert configuration.model == "test-model"
    assert configuration.timeout == 42


def test_resolve_provider_explicit_values_override_defaults(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "environment-key")
    monkeypatch.setenv(
        "OPENAI_BASE_URL",
        "https://environment.example/v1",
    )
    monkeypatch.setenv(
        "OPENAI_ORGANIZATION",
        "environment-org",
    )

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ProjectRuntime",
        lambda *root: type(
            "Runtime",
            (),
            {
                "config": type(
                    "Config",
                    (),
                    {
                        "model": "project-model",
                        "timeout": 42,
                    },
                )()
            },
        )(),
    )

    captured = {}

    def fake_create(name, configuration=None, **kwargs):
        captured["name"] = name
        captured["configuration"] = configuration
        return object()

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ProviderRegistry.create",
        fake_create,
    )

    resolve_provider(
        "openai",
        api_key="explicit-key",
        endpoint="https://explicit.example/v1",
        organization="explicit-org",
        model="explicit-model",
        timeout=99,
    )

    configuration = captured["configuration"]

    assert captured["name"] == "openai"
    assert configuration.api_key == "explicit-key"
    assert configuration.endpoint == "https://explicit.example/v1"
    assert configuration.organization == "explicit-org"
    assert configuration.model == "explicit-model"
    assert configuration.timeout == 99

def test_resolve_provider_uses_connection_metadata(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "connection-key")

    captured = {}

    def fake_create(name, configuration=None, **kwargs):
        captured["name"] = name
        captured["configuration"] = configuration
        return object()

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ProviderRegistry.create",
        fake_create,
    )

    resolve_provider("openai")

    assert captured["name"] == "openai"
    assert captured["configuration"].api_key == "connection-key"

def test_resolve_provider_uses_named_connection_credential(monkeypatch):
    captured = {}

    class FakeManifest:
        def __init__(self, path):
            assert path == (
                Path.cwd()
                / ".bindai"
                / "connections.toml"
            )

        def get(self, name):
            assert name == "work"

            return type(
                "Connection",
                (),
                {
                    "name": "work",
                    "provider": "openai",
                },
            )()

    class FakeStore:
        def get(self, name):
            assert name == "work"
            return "connection-key"

    def fake_create(name, configuration=None, **kwargs):
        captured["name"] = name
        captured["configuration"] = configuration
        return object()

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ConnectionManifest",
        FakeManifest,
    )
    monkeypatch.setattr(
        "bindai_agent.provider_resolver.KeyringProviderCredentialStore",
        FakeStore,
    )
    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ProviderRegistry.create",
        fake_create,
    )

    resolve_provider(
        "openai",
        connection="work",
    )

    assert captured["name"] == "openai"
    assert captured["configuration"].api_key == "connection-key"


def test_resolve_provider_named_connection_overrides_environment(
    monkeypatch,
):
    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "environment-key",
    )

    captured = {}

    class FakeManifest:
        def __init__(self, path):
            pass

        def get(self, name):
            return type(
                "Connection",
                (),
                {
                    "name": "work",
                    "provider": "openai",
                },
            )()

    class FakeStore:
        def get(self, name):
            return "connection-key"

    def fake_create(name, configuration=None, **kwargs):
        captured["configuration"] = configuration
        return object()

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ConnectionManifest",
        FakeManifest,
    )
    monkeypatch.setattr(
        "bindai_agent.provider_resolver.KeyringProviderCredentialStore",
        FakeStore,
    )
    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ProviderRegistry.create",
        fake_create,
    )

    resolve_provider(
        "openai",
        connection="work",
    )

    assert captured["configuration"].api_key == "connection-key"


def test_resolve_provider_explicit_api_key_overrides_connection(
    monkeypatch,
):
    captured = {}

    class FakeManifest:
        def __init__(self, path):
            pass

        def get(self, name):
            return type(
                "Connection",
                (),
                {
                    "name": "work",
                    "provider": "openai",
                },
            )()

    class FakeStore:
        def get(self, name):
            return "connection-key"

    def fake_create(name, configuration=None, **kwargs):
        captured["configuration"] = configuration
        return object()

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ConnectionManifest",
        FakeManifest,
    )
    monkeypatch.setattr(
        "bindai_agent.provider_resolver.KeyringProviderCredentialStore",
        FakeStore,
    )
    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ProviderRegistry.create",
        fake_create,
    )

    resolve_provider(
        "openai",
        connection="work",
        api_key="explicit-key",
    )

    assert captured["configuration"].api_key == "explicit-key"


def test_resolve_provider_rejects_connection_for_different_provider(
    monkeypatch,
):
    class FakeManifest:
        def __init__(self, path):
            pass

        def get(self, name):
            return type(
                "Connection",
                (),
                {
                    "name": "work",
                    "provider": "anthropic",
                },
            )()

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ConnectionManifest",
        FakeManifest,
    )

    try:
        resolve_provider(
            "openai",
            connection="work",
        )
    except ValueError as exc:
        assert str(exc) == (
            'Connection "work" uses provider '
            '"anthropic", not "openai".'
        )
    else:
        raise AssertionError(
            "Expected provider mismatch to raise ValueError.",
        )


def test_resolve_provider_rejects_missing_connection(monkeypatch):
    class FakeManifest:
        def __init__(self, path):
            pass

        def get(self, name):
            return None

    monkeypatch.setattr(
        "bindai_agent.provider_resolver.ConnectionManifest",
        FakeManifest,
    )

    try:
        resolve_provider(
            "openai",
            connection="missing",
        )
    except ValueError as exc:
        assert str(exc) == (
            'Connection "missing" is not configured.'
        )
    else:
        raise AssertionError(
            "Expected missing connection to raise ValueError.",
        )
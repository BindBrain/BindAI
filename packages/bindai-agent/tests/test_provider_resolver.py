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
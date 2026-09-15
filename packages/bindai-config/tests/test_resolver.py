from __future__ import annotations

import pytest
from bindai_config import ConfigResolver, ConfigValue, ProjectConfig


def test_resolver_uses_defaults_when_field_is_not_configured() -> None:
    resolver = ConfigResolver(
        ProjectConfig(),
        environ={},
    )

    result = resolver.resolve("model")

    assert result == ConfigValue(
        value="gpt-4.1-mini",
        source="default",
    )


def test_resolver_uses_toml_when_field_is_configured() -> None:
    config = ProjectConfig(
        model="gpt-5",
        temperature=0.7,
    )

    resolver = ConfigResolver(
        config,
        configured_fields={"model", "temperature"},
        environ={},
    )

    assert resolver.resolve("model") == ConfigValue(
        value="gpt-5",
        source="bindai.toml",
    )

    assert resolver.resolve("temperature") == ConfigValue(
        value=0.7,
        source="bindai.toml",
    )


def test_resolver_uses_toml_even_when_value_equals_default() -> None:
    config = ProjectConfig(
        temperature=0.7,
    )

    resolver = ConfigResolver(
        config,
        configured_fields={"temperature"},
        environ={},
    )

    assert resolver.resolve("temperature") == ConfigValue(
        value=0.7,
        source="bindai.toml",
    )


def test_resolver_prefers_environment_over_toml() -> None:
    config = ProjectConfig(
        model="gpt-5",
    )

    resolver = ConfigResolver(
        config,
        configured_fields={"model"},
        environ={
            "BINDAI_MODEL": "gpt-5-mini",
        },
    )

    assert resolver.resolve("model") == ConfigValue(
        value="gpt-5-mini",
        source="environment:BINDAI_MODEL",
    )


def test_resolver_converts_environment_integer() -> None:
    resolver = ConfigResolver(
        ProjectConfig(),
        environ={
            "BINDAI_TIMEOUT": "120",
        },
    )

    result = resolver.resolve("timeout")

    assert result == ConfigValue(
        value=120,
        source="environment:BINDAI_TIMEOUT",
    )


def test_resolver_converts_environment_float() -> None:
    resolver = ConfigResolver(
        ProjectConfig(),
        environ={
            "BINDAI_TEMPERATURE": "0.25",
        },
    )

    result = resolver.resolve("temperature")

    assert result == ConfigValue(
        value=0.25,
        source="environment:BINDAI_TEMPERATURE",
    )


def test_resolver_rejects_unknown_field() -> None:
    resolver = ConfigResolver(
        ProjectConfig(),
        environ={},
    )

    with pytest.raises(
        KeyError,
        match='Unknown configuration field "unknown"',
    ):
        resolver.resolve("unknown")


def test_resolver_returns_all_fields() -> None:
    resolver = ConfigResolver(
        ProjectConfig(
            name="Configured Project",
            model="gpt-5",
        ),
        configured_fields={"name", "model"},
        environ={
            "BINDAI_TIMEOUT": "90",
        },
    )

    values = resolver.all()

    assert values["name"] == ConfigValue(
        value="Configured Project",
        source="bindai.toml",
    )
    assert values["model"] == ConfigValue(
        value="gpt-5",
        source="bindai.toml",
    )
    assert values["timeout"] == ConfigValue(
        value=90,
        source="environment:BINDAI_TIMEOUT",
    )
    assert values["provider"] == ConfigValue(
        value="openai",
        source="default",
    )
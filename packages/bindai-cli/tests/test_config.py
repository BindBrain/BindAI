from pathlib import Path

from bindai_cli.app import app
from typer.testing import CliRunner

runner = CliRunner()


def test_config_list_shows_defaults(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["config", "list"],
    )

    assert result.exit_code == 0
    assert "Configuration" in result.stdout
    assert "name" in result.stdout
    assert "BindAI Project" in result.stdout
    assert "default" in result.stdout


def test_config_list_shows_toml_values_and_sources(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "bindai.toml").write_text(
        """
name = "test-project"
provider = "anthropic"
model = "claude-test"
temperature = 0.2
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["config", "list"],
    )

    assert result.exit_code == 0
    assert "test-project" in result.stdout
    assert "anthropic" in result.stdout
    assert "claude-test" in result.stdout
    assert "0.2" in result.stdout
    assert "bindai.toml" in result.stdout


def test_config_list_shows_environment_override(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "bindai.toml").write_text(
        """
provider = "openai"
""".strip(),
        encoding="utf-8",
    )

    monkeypatch.setenv(
        "BINDAI_PROVIDER",
        "anthropic",
    )

    result = runner.invoke(
        app,
        ["config", "list"],
    )

    assert result.exit_code == 0
    assert "anthropic" in result.stdout
    assert "environment:BINDAI_PROVIDER" in result.stdout


def test_config_help_lists_list_command():
    result = runner.invoke(
        app,
        ["config", "--help"],
    )

    assert result.exit_code == 0
    assert "list" in result.stdout


def test_config_get_shows_default_value_and_source(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["config", "get", "provider"],
    )

    assert result.exit_code == 0
    assert "provider = openai" in result.stdout
    assert "source = default" in result.stdout


def test_config_get_shows_toml_value_and_source(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "bindai.toml").write_text(
        """
provider = "anthropic"
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["config", "get", "provider"],
    )

    assert result.exit_code == 0
    assert "provider = anthropic" in result.stdout
    assert "source = bindai.toml" in result.stdout


def test_config_get_shows_environment_override(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "bindai.toml").write_text(
        """
provider = "openai"
""".strip(),
        encoding="utf-8",
    )

    monkeypatch.setenv(
        "BINDAI_PROVIDER",
        "anthropic",
    )

    result = runner.invoke(
        app,
        ["config", "get", "provider"],
    )

    assert result.exit_code == 0
    assert "provider = anthropic" in result.stdout
    assert "source = environment:BINDAI_PROVIDER" in result.stdout


def test_config_get_rejects_unknown_field(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["config", "get", "unknown"],
    )

    assert result.exit_code != 0
    assert 'Unknown configuration field "unknown".' in result.output


def test_config_path_shows_bindai_toml_path(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        'provider = "openai"\n',
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["config", "path"],
    )

    assert result.exit_code == 0
    assert "bindai.toml" in result.stdout
    assert str(tmp_path) in result.stdout.replace("\n", "")


def test_config_path_fails_when_bindai_toml_is_missing(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["config", "path"],
    )

    assert result.exit_code != 0
    assert "No bindai.toml found in" in result.output
    assert "bindai.toml" in result.output


def test_config_help_lists_path_command():
    result = runner.invoke(
        app,
        ["config", "--help"],
    )

    assert result.exit_code == 0
    assert "list" in result.stdout
    assert "get" in result.stdout
    assert "path" in result.stdout


def test_config_set_updates_existing_string_value(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
provider = "openai"
model = "gpt-4.1-mini"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["config", "set", "provider", "anthropic"],
    )

    assert result.exit_code == 0
    assert 'provider = "anthropic"' in config_path.read_text(
        encoding="utf-8",
    )


def test_config_set_updates_typed_values(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        'temperature = 0.7\n',
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["config", "set", "temperature", "0.3"],
    )

    assert result.exit_code == 0

    content = config_path.read_text(encoding="utf-8")
    assert "temperature = 0.3" in content


def test_config_set_adds_missing_known_field(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        'provider = "openai"\n',
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["config", "set", "timeout", "120"],
    )

    assert result.exit_code == 0

    content = config_path.read_text(encoding="utf-8")
    assert 'provider = "openai"' in content
    assert "timeout = 120" in content


def test_config_set_preserves_comments_and_unrelated_content(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
# Project configuration
name = "demo"

# Model configuration
provider = "openai" # Current provider
model = "gpt-4.1-mini"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["config", "set", "provider", "anthropic"],
    )

    assert result.exit_code == 0

    content = config_path.read_text(encoding="utf-8")
    assert "# Project configuration" in content
    assert "# Model configuration" in content
    assert 'provider = "anthropic" # Current provider' in content
    assert 'model = "gpt-4.1-mini"' in content


def test_config_set_rejects_unknown_field_without_modifying_file(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_path = tmp_path / "bindai.toml"
    original = 'provider = "openai"\n'
    config_path.write_text(original, encoding="utf-8")

    result = runner.invoke(
        app,
        ["config", "set", "unknown", "value"],
    )

    assert result.exit_code != 0
    assert 'Unknown configuration field "unknown".' in result.output
    assert config_path.read_text(encoding="utf-8") == original


def test_config_set_rejects_invalid_value_without_modifying_file(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_path = tmp_path / "bindai.toml"
    original = "temperature = 0.7\n"
    config_path.write_text(original, encoding="utf-8")

    result = runner.invoke(
        app,
        ["config", "set", "temperature", "not-a-number"],
    )

    assert result.exit_code != 0
    assert "Invalid value" in result.output
    assert config_path.read_text(encoding="utf-8") == original


def test_config_set_requires_bindai_toml(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["config", "set", "provider", "anthropic"],
    )

    assert result.exit_code != 0
    assert "No bindai.toml found in" in result.output


def test_config_set_only_changes_toml_when_environment_overrides_value(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        'provider = "openai"\n',
        encoding="utf-8",
    )

    monkeypatch.setenv(
        "BINDAI_PROVIDER",
        "anthropic",
    )

    result = runner.invoke(
        app,
        ["config", "set", "provider", "google"],
    )

    assert result.exit_code == 0
    assert 'provider = "google"' in config_path.read_text(
        encoding="utf-8",
    )

    get_result = runner.invoke(
        app,
        ["config", "get", "provider"],
    )

    assert get_result.exit_code == 0
    assert "provider = anthropic" in get_result.stdout
    assert "source = environment:BINDAI_PROVIDER" in get_result.stdout


def test_config_help_lists_set_command():
    result = runner.invoke(
        app,
        ["config", "--help"],
    )

    assert result.exit_code == 0
    assert "list" in result.stdout
    assert "get" in result.stdout
    assert "path" in result.stdout
    assert "set" in result.stdout

def test_config_set_updates_connection_value(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    config_path = tmp_path / "bindai.toml"
    config_path.write_text(
        """
provider = "openai"
model = "gpt-4.1-mini"
""".strip()
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["config", "set", "connection", "work"],
    )

    assert result.exit_code == 0

    content = config_path.read_text(encoding="utf-8")
    assert 'connection = "work"' in content
    assert 'provider = "openai"' in content
    assert 'model = "gpt-4.1-mini"' in content
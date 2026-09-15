from pathlib import Path

from bindai_cli.app import app
from typer.testing import CliRunner

runner = CliRunner()


def test_connections_help_lists_add():
    result = runner.invoke(
        app,
        ["connections", "--help"],
    )

    assert result.exit_code == 0
    assert "add" in result.stdout


def test_connections_add_stores_credential_and_manifest(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    stored: dict[tuple[str, str], str] = {}

    class FakeKeyring:
        def set_password(
            self,
            service: str,
            username: str,
            password: str,
        ) -> None:
            stored[(service, username)] = password

        def get_password(
            self,
            service: str,
            username: str,
        ) -> str | None:
            return stored.get((service, username))

        def delete_password(
            self,
            service: str,
            username: str,
        ) -> None:
            stored.pop((service, username), None)

    monkeypatch.setattr(
        "bindai_connections.keyring_credentials.KeyringProviderCredentialStore._keyring",
        staticmethod(lambda: FakeKeyring()),
    )

    result = runner.invoke(
        app,
        ["connections", "add", "openai"],
        input="secret-key\n",
    )

    assert result.exit_code == 0
    assert 'Connection "openai" added for provider "openai".' in result.stdout

    assert stored[("bindai", "openai")] == "secret-key"

    manifest = (
        tmp_path
        / ".bindai"
        / "connections.toml"
    )

    assert manifest.exists()

    content = manifest.read_text(encoding="utf-8")

    assert 'name = "openai"' in content
    assert 'provider = "openai"' in content
    assert "secret-key" not in content


def test_connections_add_supports_custom_name(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    class FakeKeyring:
        def set_password(self, service, username, password):
            pass

    monkeypatch.setattr(
        "bindai_connections.keyring_credentials.KeyringProviderCredentialStore._keyring",
        staticmethod(lambda: FakeKeyring()),
    )

    result = runner.invoke(
        app,
        [
            "connections",
            "add",
            "openai",
            "--name",
            "work",
        ],
        input="secret-key\n",
    )

    assert result.exit_code == 0

    manifest = (
        tmp_path
        / ".bindai"
        / "connections.toml"
    )

    content = manifest.read_text(encoding="utf-8")

    assert 'name = "work"' in content
    assert 'provider = "openai"' in content


def test_connections_add_rejects_unknown_provider(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["connections", "add", "unknown"],
    )

    assert result.exit_code != 0
    assert 'Unknown provider "unknown".' in result.output


def test_connections_add_rejects_empty_name(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        [
            "connections",
            "add",
            "openai",
            "--name",
            "   ",
        ],
    )

    assert result.exit_code != 0
    assert "Connection name cannot be empty." in result.output
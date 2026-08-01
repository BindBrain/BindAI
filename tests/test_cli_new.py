from pathlib import Path

from bindai_cli.app import app
from typer.testing import CliRunner

runner = CliRunner()


def test_bindai_new(tmp_path: Path):
    project = tmp_path / "Demo"

    result = runner.invoke(
        app,
        [
            "new",
            str(project),
        ],
    )

    assert result.exit_code == 0

    assert (project / "bindai.toml").exists()
    assert (project / "README.md").exists()
    assert (project / "LICENSE").exists()
    assert (project / "main.py").exists()

    assert (project / "agents").exists()
    assert (project / "knowledge").exists()
    assert (project / "memory").exists()
    assert (project / "templates").exists()
    assert (project / "tools").exists()
    assert (project / "workflows").exists()

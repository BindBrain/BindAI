from __future__ import annotations

from pathlib import Path

from bindai_config.tool_loader import ToolLoader


def test_tool_loader_returns_empty_list_when_tools_directory_is_missing(
    tmp_path: Path,
) -> None:
    assert ToolLoader.load(tmp_path) == []

def test_tool_loader_ignores_underscore_prefixed_files(
    tmp_path: Path,
) -> None:
    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()

    (tools_dir / "_private.py").write_text(
        """
raise RuntimeError("This file should not be imported")
""".strip()
        + "\n",
        encoding="utf-8",
    )

    assert ToolLoader.load(tmp_path) == []

def test_tool_loader_loads_decorated_tools(
    tmp_path: Path,
) -> None:
    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()

    (tools_dir / "example.py").write_text(
        """
from bindai import tool


@tool(
    name="example",
    description="An example tool.",
)
def example_tool(value: str) -> str:
    return value.upper()
""".strip()
        + "\n",
        encoding="utf-8",
    )

    tools = ToolLoader.load(tmp_path)

    assert len(tools) == 1
    assert tools[0].name == "example"
    assert tools[0].description == "An example tool."
    assert tools[0].function("hello") == "HELLO"

def test_tool_loader_ignores_non_tool_objects(
    tmp_path: Path,
) -> None:
    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()

    (tools_dir / "helper.py").write_text(
        """
VALUE = "not a tool"


def helper(value: str) -> str:
    return value.upper()
""".strip()
        + "\n",
        encoding="utf-8",
    )

    assert ToolLoader.load(tmp_path) == []

from __future__ import annotations

from pathlib import Path

import pytest
from bindai_config.yaml_loader import YamlLoader


def test_yaml_loader_rejects_unknown_agent(tmp_path: Path) -> None:
    config_path = tmp_path / "group.yaml"
    config_path.write_text(
        """
group:
  name: Example Group
  agents:
    - id: researcher
      name: Researcher
      instructions: Research the topic.
  tasks:
    - id: research
      description: Research the topic.
      agent: missing-agent
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match='Unknown agent "missing-agent"',
    ):
        YamlLoader().load(config_path)


def test_yaml_loader_rejects_unknown_task_dependency(tmp_path: Path) -> None:
    config_path = tmp_path / "group.yaml"
    config_path.write_text(
        """
group:
  name: Example Group
  agents:
    - id: researcher
      name: Researcher
      instructions: Research the topic.
  tasks:
    - id: research
      description: Research the topic.
      agent: researcher
      context:
        - missing-task
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match='Unknown task "missing-task"',
    ):
        YamlLoader().load(config_path)

def test_yaml_loader_rejects_unknown_process(tmp_path: Path) -> None:
    config_path = tmp_path / "group.yaml"
    config_path.write_text(
        """
group:
  name: Example Group
  process: invalid
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match='Unknown group process "invalid"',
    ):
        YamlLoader().load(config_path)
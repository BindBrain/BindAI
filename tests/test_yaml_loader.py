from pathlib import Path

import pytest

from bindai import YamlLoader
from bindai_group import ParallelProcess, SequentialProcess


def test_yaml_loader():

    group = YamlLoader().load(
        "examples/assets/marketing.yaml",
    )

    assert group is not None

    assert len(group.agents) == 2

    assert len(group.tasks) == 2


def test_yaml_loader_uses_sequential_process(tmp_path: Path):

    yaml_file = tmp_path / "group.yaml"

    yaml_file.write_text(
        """
group:
  name: Sequential Group
  process: sequential

  agents:
    - id: researcher
      name: Research Agent
      provider: openai
      model: gpt-4.1
      instructions: Research.

  tasks:
    - id: research
      description: Research OpenAI.
      agent: researcher
""",
        encoding="utf-8",
    )

    group = YamlLoader().load(
        str(yaml_file),
    )

    assert isinstance(
        group.process,
        SequentialProcess,
    )


def test_yaml_loader_uses_parallel_process(tmp_path: Path):

    yaml_file = tmp_path / "group.yaml"

    yaml_file.write_text(
        """
group:
  name: Parallel Group
  process: parallel

  agents:
    - id: researcher
      name: Research Agent
      provider: openai
      model: gpt-4.1
      instructions: Research.

  tasks:
    - id: research
      description: Research OpenAI.
      agent: researcher
""",
        encoding="utf-8",
    )

    group = YamlLoader().load(
        str(yaml_file),
    )

    assert isinstance(
        group.process,
        ParallelProcess,
    )


def test_yaml_loader_rejects_unknown_process(tmp_path: Path):

    yaml_file = tmp_path / "group.yaml"

    yaml_file.write_text(
        """
group:
  name: Invalid Group
  process: invalid

  agents:
    - id: researcher
      name: Research Agent
      provider: openai
      model: gpt-4.1
      instructions: Research.

  tasks:
    - id: research
      description: Research OpenAI.
      agent: researcher
""",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match='Unknown group process "invalid"',
    ):
        YamlLoader().load(
            str(yaml_file),
        )
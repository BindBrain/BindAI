from bindai import (
    AgentBuilder,
    GroupBuilder,
)


def test_agent_builder():

    builder = AgentBuilder()

    assert builder is not None


def test_group_builder():

    builder = GroupBuilder()

    assert builder is not None
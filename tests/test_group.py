import pytest

from bindai import GroupBuilder


def test_group_requires_agent():

    with pytest.raises(
        ValueError,
    ):
        (GroupBuilder().name("Test").build())

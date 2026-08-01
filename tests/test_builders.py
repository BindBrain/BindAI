import pytest

from bindai import AgentBuilder


def test_model_requires_provider_prefix():

    builder = AgentBuilder()

    with pytest.raises(
        ValueError,
        match="Model must be in the format",
    ):
        builder.model("gpt-5")


def test_model_requires_provider_name():

    builder = AgentBuilder()

    with pytest.raises(
        ValueError,
        match="Provider name cannot be empty",
    ):
        builder.model(":gpt-5")


def test_model_requires_model_name():

    builder = AgentBuilder()

    with pytest.raises(
        ValueError,
        match="Model name cannot be empty",
    ):
        builder.model("openai:")
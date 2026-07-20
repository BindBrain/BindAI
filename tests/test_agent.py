from bindai import AgentBuilder


def test_agent_builder_name():

    builder = (
        AgentBuilder()
        .name("Assistant")
    )

    assert builder is not None
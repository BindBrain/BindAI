from bindai import (
    Agent,
    AgentBuilder,
    Application,
    Group,
    Memory,
    Tool,
    Workflow,
)


def test_public_api_exports():
    assert Agent.__name__ == "Agent"
    assert AgentBuilder.__name__ == "AgentBuilder"
    assert Application.__name__ == "Application"
    assert Group.__name__ == "Group"
    assert Memory.__name__ == "Memory"
    assert Tool.__name__ == "Tool"
    assert Workflow.__name__ == "Workflow"
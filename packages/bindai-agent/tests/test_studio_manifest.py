from bindai_agent.nodes import (
    AgentNode,
    NodeRegistry,
)

from bindai_agent.studio import (
    get_node_manifest,
)


class ManifestTestNode(AgentNode):

    def __init__(self):
        super().__init__(
            "manifest_test",
            "Manifest test node",
        )

    def inputs(self):
        return [
            {
                "name": "message",
                "type": "string",
            }
        ]

    def outputs(self):
        return [
            {
                "name": "result",
                "type": "string",
            }
        ]

    def config_schema(self):
        return {
            "message": {
                "type": "string",
                "required": True,
            },
        }

    def execute(
        self,
        agent,
        context,
    ):
        return None


NodeRegistry.register(
    "manifest_test",
    ManifestTestNode,
)


def test_manifest_contains_config_schema():

    manifest = get_node_manifest()

    entry = next(
        node
        for node in manifest
        if node["type"] == "manifest_test"
    )

    assert entry["name"] == "manifest_test"

    assert entry["config_schema"] == {
        "message": {
            "type": "string",
            "required": True,
        },
    }

from __future__ import annotations

from bindai_agent.nodes import NodeRegistry


def get_node_manifest():

    manifest = []

    for node_type in NodeRegistry.available():

        node = NodeRegistry.create(
            node_type,
        )

        manifest.append(
            {
                "type": node_type,
                "name": node.name,
                "description": node.description,
                "inputs": node.inputs(),
                "outputs": node.outputs(),
                "config_schema": node.config_schema(),
            }
        )

    return manifest

from __future__ import annotations

from .registry import NodeRegistry


def node_type(
    name: str,
):
    """
    Register a Studio node type.
    """

    def decorator(cls):

        NodeRegistry.register(
            name,
            cls,
        )

        return cls

    return decorator

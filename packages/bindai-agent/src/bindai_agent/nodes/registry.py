from __future__ import annotations

from typing import Type

from .node import AgentNode


class NodeRegistry:
    """
    Registry for Studio node types.
    """

    _nodes: dict[str, Type[AgentNode]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        node: Type[AgentNode],
    ) -> None:

        cls._nodes[name] = node


    @classmethod
    def create(
        cls,
        name: str,
        **kwargs,
    ) -> AgentNode:

        node = cls._nodes[name]

        return node(
            **kwargs,
        )


    @classmethod
    def available(
        cls,
    ) -> list[str]:

        return list(
            cls._nodes.keys()
        )

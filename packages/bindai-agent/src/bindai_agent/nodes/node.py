from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bindai_core.context import ExecutionContext
    from bindai_agent.agent import Agent


class AgentNode(ABC):
    """
    Studio compatible node.

    A node is a visual execution unit.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
    ):
        self.name = name
        self.description = description


    def inputs(
        self,
    ):
        """
        Studio input ports.
        """

        return []


    def outputs(
        self,
    ):
        """
        Studio output ports.
        """

        return []


    def config_schema(
        self,
    ):
        """
        Studio configuration schema.

        Nodes may override this to describe
        supported configuration fields.
        """

        return {}


    @abstractmethod
    def execute(
        self,
        agent: Agent,
        context: ExecutionContext,
    ):
        ...

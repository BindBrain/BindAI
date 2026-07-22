from __future__ import annotations

from .container import BindContainer


class ServiceScope:
    """
    Represents one dependency injection scope.

    Future versions will use this for:

    - HTTP Request
    - Workflow execution
    - Agent execution
    - MCP session

    v1 only delegates to the root container.
    """

    def __init__(
        self,
        container: BindContainer,
    ):

        self.container = container

    def resolve(
        self,
        service_type,
    ):

        return self.container.resolve(
            service_type,
        )

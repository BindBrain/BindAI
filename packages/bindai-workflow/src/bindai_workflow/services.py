from __future__ import annotations

from bindai_core.container import BindContainer


class WorkflowServices:
    """
    Dependency injection helper
    available during workflow execution.
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

    def try_resolve(
        self,
        service_type,
    ):

        try:
            return self.resolve(
                service_type,
            )

        except Exception:
            return None

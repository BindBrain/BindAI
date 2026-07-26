from __future__ import annotations


class ToolException(Exception):
    """
    Base tool exception.
    """


class ToolNotFound(
    ToolException,
):
    def __init__(
        self,
        name: str,
    ):

        super().__init__(f"Tool '{name}' is not registered.")


class ToolAlreadyRegistered(
    ToolException,
):
    def __init__(
        self,
        name: str,
    ):

        super().__init__(f"Tool '{name}' is already registered.")

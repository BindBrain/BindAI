from __future__ import annotations

from bindai_agent import Agent


class Task:
    """
    Represents one unit of work.
    """

    def __init__(
        self,
        *,
        description: str,
        agent: Agent,
        expected_output: str | None = None,
    ):

        self.description = description

        self.agent = agent

        self.expected_output = expected_output

        self.result = None
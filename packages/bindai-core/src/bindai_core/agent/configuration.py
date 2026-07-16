from __future__ import annotations


class AgentConfiguration:
    """
    Configuration for an agent.
    """

    def __init__(self):

        self.name = ""

        self.description = ""

        self.instructions = ""

        self.model = None

        self.temperature = 0.7

        self.max_tokens = None
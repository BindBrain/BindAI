from __future__ import annotations

from .agent import Agent


class AssistantAgent(Agent):
    """
    General-purpose conversational agent.
    """

    @staticmethod
    def builder():
        from .builder import AgentBuilder

        return AgentBuilder()

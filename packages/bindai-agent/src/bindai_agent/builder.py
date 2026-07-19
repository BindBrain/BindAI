from __future__ import annotations

from bindai_core.provider import ProviderConfiguration
from bindai_provider_openai import OpenAIProvider

from .assistant import AssistantAgent


class AgentBuilder:

    def __init__(self):

        self._provider = None
        self._name = "assistant"
        self._instructions = ""
        self._tools = []

    def openai(
        self,
        api_key: str,
        model: str,
    ):

        self._provider = OpenAIProvider(
            ProviderConfiguration(
                api_key=api_key,
                model=model,
            )
        )

        return self

    def name(
        self,
        value: str,
    ):

        self._name = value
        return self

    def instructions(
        self,
        value: str,
    ):

        self._instructions = value
        return self

    def tool(
        self,
        tool,
    ):

        self._tools.append(tool)

        return self

    def build(
        self,
    ):

        agent = AssistantAgent(
            name=self._name,
            instructions=self._instructions,
            provider=self._provider,
        )

        for tool in self._tools:

            agent.tools.register(tool)

        return agent
from __future__ import annotations

import os

from bindai_prompts import Prompt

from dotenv import load_dotenv

from bindai_core.model import ModelProvider
from bindai_core.provider import ProviderConfiguration
from bindai_provider_openai import OpenAIProvider

from .assistant import AssistantAgent
from .configuration import AgentConfiguration


class AgentBuilder:
    def __init__(self):

        self._provider = None

        self._name = "assistant"

        self._prompt = Prompt()

        self._tools = []

        self._memory = None

        self._retriever = None

        self._knowledge = None

        self._middleware = []

        self._hooks = []

        self._configuration = AgentConfiguration()

    #
    # Providers
    #

    def openai(
        self,
        model: str,
    ):

        load_dotenv()

        self._provider = OpenAIProvider(
            ProviderConfiguration(
                api_key=os.getenv(
                    "OPENAI_API_KEY",
                ),
                organization=os.getenv(
                    "OPENAI_ORGANIZATION",
                ),
                endpoint=os.getenv(
                    "OPENAI_BASE_URL",
                ),
                model=model,
            )
        )

        return self

    def provider(
        self,
        provider: ModelProvider,
    ):

        self._provider = provider

        return self

    #
    # Basic settings
    #

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

        self._prompt.system = value

        return self

    #
    # Agent configuration
    #

    def temperature(
        self,
        value: float,
    ):

        self._configuration.temperature = value

        return self

    def max_tokens(
        self,
        value: int,
    ):

        self._configuration.max_tokens = value

        return self

    def max_tool_iterations(
        self,
        value: int,
    ):

        self._configuration.max_tool_iterations = value

        return self

    #
    # Components
    #

    def tool(
        self,
        tool,
    ):

        self._tools.append(tool)

        return self

    def memory(
        self,
        memory,
    ):

        self._memory = memory

        return self

    def retriever(
        self,
        retriever,
    ):

        self._retriever = retriever

        return self

    def knowledge(
        self,
        knowledge,
    ):

        self._knowledge = knowledge

        return self

    def middleware(
        self,
        middleware,
    ):

        self._middleware.append(
            middleware,
        )

        return self

    def hook(
        self,
        hook,
    ):

        self._hooks.append(
            hook,
        )

        return self

    #
    # Build
    #

    def build(
        self,
    ):

        if self._provider is None:
            raise ValueError(
                "No provider configured. Use .provider(...) or .openai(...)."
            )

        agent = AssistantAgent(
            name=self._name,
            instructions=self._prompt.system,
            provider=self._provider,
        )

        #
        # Configuration
        #

        agent.configuration = self._configuration

        #
        # Tools
        #

        for tool in self._tools:
            agent.tool(
                tool,
            )

        #
        # Memory
        #

        if self._memory is not None:
            agent.use_memory(
                self._memory,
            )

        #
        # Knowledge
        #

        if self._retriever is not None:
            agent.use_retriever(
                self._retriever,
            )

        if self._knowledge is not None:
            agent.use_knowledge(
                self._knowledge,
            )

        #
        # Middleware
        #

        for middleware in self._middleware:
            agent.use_middleware(
                middleware,
            )

        #
        # Hooks
        #

        for hook in self._hooks:
            agent.hook(
                hook,
            )

        return agent

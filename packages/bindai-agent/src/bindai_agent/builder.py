from __future__ import annotations

import os
from pathlib import Path

from bindai_config.runtime import ProjectRuntime
from bindai_config.tool_loader import ToolLoader
from bindai_core.events import EventBus
from bindai_core.provider import ModelProvider
from bindai_prompts import Prompt
from bindai_providers import (
    ProviderConfiguration,
    ProviderRegistry,
)
from bindai_tool.function_tool import FunctionTool
from dotenv import load_dotenv

from .assistant import AssistantAgent
from .configuration import AgentConfiguration
from .registry import AgentRegistry


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

        self._events = EventBus()

    #
    # Providers
    #

    def openai(
        self,
        model: str,
    ):

        load_dotenv()

        return self.provider(
            "openai",
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

    def provider(
        self,
        provider: str | ModelProvider,
        *,
        api_key: str | None = None,
        endpoint: str | None = None,
        organization: str | None = None,
        model: str | None = None,
    ):

        """
    Configure the provider.

    Accepts either:

    - a registered provider name (e.g. "openai", "anthropic", "ollama")
    - an instantiated ModelProvider
    """

        if isinstance(
            provider,
            str,
        ):
            configuration = ProviderConfiguration(
                api_key=api_key,
                endpoint=endpoint,
                organization=organization,
                model=model,
            )

            self._provider = ProviderRegistry.create(
                provider,
                configuration=configuration,
            )

        else:
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
            runtime = ProjectRuntime(
                Path.cwd(),
            )

            self.model(f"{runtime.config.provider}:{runtime.config.model}")

            self.temperature(runtime.config.temperature)

        agent = AssistantAgent(
            name=self._name,
            instructions=self._prompt.system,
            provider=self._provider,
        )

        agent.events = self._events
        #
        # Configuration
        #

        agent.configuration = self._configuration

        #
        # Tools
        #

        for tool in self._tools:
            agent.tool(tool)

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

        AgentRegistry.register(
            agent,
        )

        return agent

    def events(
        self,
        events: EventBus,
    ):

        self._events = events

        return self

    def tools(
        self,
        *tools,
    ):

        for tool in tools:
            if callable(tool) and not isinstance(tool, FunctionTool):
                tool = FunctionTool(tool)

            self._tools.append(tool)

        return self

    def model(
        self,
        value: str,
    ):
        """
        Accepts either:

        openai:gpt-4.1-mini
        openai:gpt-5
        anthropic:claude-sonnet-4
        ollama:llama3
        lmstudio:qwen3
        """

        provider, model = value.split(
            ":",
            1,
        )

        if provider == "openai":
            return self.openai(model)

        return self.provider(
            provider,
            model=model,
        )

    def from_project(
        self,
        root: str | Path = ".",
    ):

        runtime = ProjectRuntime(
            Path(root),
        )

        config = runtime.config

        self.tools(
            *ToolLoader.load(
                Path(root),
            ),
        )

        self.model(
            f"{config.provider}:{config.model}",
        )

        self.temperature(
            config.temperature,
        )

        return self

from __future__ import annotations

from pathlib import Path
from typing import Any

from bindai_config.runtime import ProjectRuntime
from bindai_config.tool_loader import ToolLoader
from bindai_core.events import EventBus
from bindai_core.provider import ModelProvider
from bindai_prompts import Prompt
from bindai_tool.function_tool import FunctionTool
from bindai_tool.tool import Tool

from .assistant import AssistantAgent
from .configuration import AgentConfiguration
from .provider_resolver import resolve_provider
from .registry import AgentRegistry


class AgentBuilder:
    def __init__(self):
        self._provider: ModelProvider | None = None
        self._name: str = "assistant"
        self._prompt: Prompt = Prompt()
        self._tools: list[FunctionTool] = []
        self._memory: Any | None = None
        self._retriever: Any | None = None
        self._knowledge: Any | None = None
        self._middleware: list[Any] = []
        self._hooks: list[Any] = []
        self._configuration: AgentConfiguration = AgentConfiguration()
        self._events: EventBus = EventBus()

    # ------------------------------------------------------------------
    # Providers
    # ------------------------------------------------------------------

    def openai(
        self,
        model: str,
        *,
        connection: str | None = None,
    ) -> AgentBuilder:
        return self.provider(
            "openai",
            model=model,
            connection=connection,
        )

    def provider(
        self,
        provider: str | ModelProvider,
        *,
        api_key: str | None = None,
        endpoint: str | None = None,
        organization: str | None = None,
        model: str | None = None,
        connection: str | None = None,
    ) -> AgentBuilder:
        """
        Configure the provider.

        Accepts either:

        - a registered provider name (e.g. "openai", "anthropic", "ollama")
        - an instantiated ModelProvider

        String provider names are resolved through the centralized provider
        resolver so provider-specific environment configuration is handled
        consistently.
        """
        if isinstance(
            provider,
            str,
        ):
            self._provider = resolve_provider(
                provider,
                api_key=api_key,
                endpoint=endpoint,
                organization=organization,
                model=model,
                connection=connection,
            )
        else:
            self._provider = provider

        return self

    # ------------------------------------------------------------------
    # Basic settings
    # ------------------------------------------------------------------

    def name(
        self,
        value: str,
    ) -> AgentBuilder:
        self._name = value
        return self

    def instructions(
        self,
        value: str,
    ) -> AgentBuilder:
        self._prompt.system = value
        return self

    # ------------------------------------------------------------------
    # Agent configuration
    # ------------------------------------------------------------------

    def temperature(
        self,
        value: float,
    ) -> AgentBuilder:
        self._configuration.temperature = value
        return self

    def max_tokens(
        self,
        value: int,
    ) -> AgentBuilder:
        self._configuration.max_tokens = value
        return self

    def max_tool_iterations(
        self,
        value: int,
    ) -> AgentBuilder:
        self._configuration.max_tool_iterations = value
        return self

    # ------------------------------------------------------------------
    # Components
    # ------------------------------------------------------------------

    def memory(
        self,
        memory: Any,
    ) -> AgentBuilder:
        self._memory = memory
        return self

    def retriever(
        self,
        retriever: Any,
    ) -> AgentBuilder:
        self._retriever = retriever
        return self

    def knowledge(
        self,
        knowledge: Any,
    ) -> AgentBuilder:
        self._knowledge = knowledge
        return self

    def middleware(
        self,
        middleware: Any,
    ) -> AgentBuilder:
        self._middleware.append(
            middleware,
        )
        return self

    def hook(
        self,
        hook: Any,
    ) -> AgentBuilder:
        self._hooks.append(
            hook,
        )
        return self

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(
        self,
    ) -> AssistantAgent:
        if self._provider is None:
            runtime = ProjectRuntime(
                Path.cwd(),
            )

            self.model(
                f"{runtime.config.provider}:{runtime.config.model}",
                connection=runtime.config.connection,
            )

            self.temperature(
                runtime.config.temperature,
            )

        agent = AssistantAgent(
            name=self._name,
            instructions=self._prompt.system or "",
            provider=self._provider,
        )

        agent.events = self._events

        # ------------------------------------------------------------------
        # Configuration
        # ------------------------------------------------------------------

        agent.configuration = self._configuration

        # ------------------------------------------------------------------
        # Tools
        # ------------------------------------------------------------------

        for tool in self._tools:
            agent.tool(
                tool,
            )

        # ------------------------------------------------------------------
        # Memory
        # ------------------------------------------------------------------

        if self._memory is not None:
            agent.use_memory(
                self._memory,
            )

        # ------------------------------------------------------------------
        # Knowledge
        # ------------------------------------------------------------------

        if self._retriever is not None:
            agent.use_retriever(
                self._retriever,
            )

        if self._knowledge is not None:
            agent.use_knowledge(
                self._knowledge,
            )

        # ------------------------------------------------------------------
        # Middleware
        # ------------------------------------------------------------------

        for middleware in self._middleware:
            agent.use_middleware(
                middleware,
            )

        # ------------------------------------------------------------------
        # Hooks
        # ------------------------------------------------------------------

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
    ) -> AgentBuilder:
        self._events = events
        return self

    def tools(
        self,
        *tools: Any,
    ) -> AgentBuilder:
        for tool in tools:
            if not isinstance(
                tool,
                Tool,
            ):
                tool = FunctionTool(
                    tool,
                )

            self._tools.append(
                tool,
            )

        return self

    def model(
        self,
        value: str,
        *,
        connection: str | None = None,
    ) -> AgentBuilder:
        """
        Configure the provider from a ``"<provider>:<model>"`` string.

        Examples:

        - ``openai:gpt-5``
        - ``openai:gpt-4.1-mini``
        - ``anthropic:claude-sonnet-4``
        - ``ollama:llama3``
        - ``lmstudio:qwen3``
        """
        try:
            provider, model = value.split(
                ":",
                1,
            )
        except ValueError as exc:
            raise ValueError(
                "Model must be in the format '<provider>:<model>'. Example: 'openai:gpt-5'."
            ) from exc

        if not provider:
            raise ValueError(
                "Provider name cannot be empty.",
            )

        if not model:
            raise ValueError(
                "Model name cannot be empty.",
            )

        if provider == "openai":
            return self.openai(
                model,
                connection=connection,
            )

        return self.provider(
            provider,
            model=model,
            connection=connection,
        )

    def from_project(
        self,
        root: str | Path = ".",
    ) -> AgentBuilder:
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
            connection=config.connection,
        )

        self.temperature(
            config.temperature,
        )

        return self
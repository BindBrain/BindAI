from __future__ import annotations

from typing import TYPE_CHECKING

from bindai_core.context import ExecutionContext

from .execution.memory_step import MemoryStep
from .execution.knowledge_step import KnowledgeStep
from .execution.prompt_builder import PromptBuilder
from .execution.tool_executor import ToolExecutor
from .execution.finish_step import FinishStep

from .execution.pipeline import ExecutionPipeline
from .execution.initialization_step import InitializationStep
from .execution.model_generation_step import ModelGenerationStep

from bindai_core.model import (
    ModelRequest,
    ModelResponse,
)

from .result import AgentResult

if TYPE_CHECKING:
    from .agent import Agent


class AgentExecutor:
    """
    Executes an agent by driving the full execution loop.
    """

    memory = MemoryStep()

    knowledge = KnowledgeStep()

    prompt_builder = PromptBuilder()

    tool_executor = ToolExecutor()

    finish_step = FinishStep()

    pipeline = ExecutionPipeline(
        InitializationStep(),
        ModelGenerationStep(),
    )

    def execute(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> AgentResult:

        self.pipeline.execute(
            agent,
            context,
        )

        for middleware in agent.middleware:
            middleware.before_execute(
                agent,
                context,
            )

        for hook in agent.hooks:
            hook.on_start(
                agent,
                context,
            )

        while True:
            request = self.prompt_builder.build(
                agent,
                context,
            )

            for hook in agent.hooks:
                hook.on_model_request(
                    request,
                )

            response = self._generate(
                agent,
                request,
            )

            for hook in agent.hooks:
                hook.on_model_response(
                    response,
                )

            if not response.tool_calls:
                result = self.finish_step.finish(
                    agent,
                    context,
                    response,
                    self.memory,
                )

                for middleware in reversed(
                    agent.middleware,
                ):
                    middleware.after_execute(
                        agent,
                        context,
                        result,
                    )

                return result

            self.tool_executor.execute(
                agent,
                response,
            )

    def stream(
        self,
        agent: Agent,
        context: ExecutionContext,
    ):

        self.pipeline.execute(
            agent,
            context,
        )

        request = self.prompt_builder.build(
            agent,
            context,
        )

        content = ""

        for chunk in agent.provider.stream(
            request,
        ):
            content += chunk.delta

            yield chunk

        agent.conversation.add_assistant(
            content,
        )

    def _initialize(
        self,
        agent: Agent,
        context: ExecutionContext,
    ) -> None:

        user_input = context.variables.get(
            "input",
            "",
        )

        from .bootstrap import register_agent_services

        register_agent_services(
            context.container,
        )

        memory = context.container.resolve(
            MemoryStep,
        )

        knowledge = context.container.resolve(
            KnowledgeStep,
        )

        if len(agent.conversation) == 0:
            agent.conversation.add_system(
                agent.instructions,
            )

            memory.load(
                agent,
            )

        agent.conversation.add_user(
            user_input,
        )

        knowledge.inject(
            agent,
            user_input,
        )

    def _generate(
        self,
        agent: Agent,
        request: ModelRequest,
    ) -> ModelResponse:

        return agent.provider.generate(
            request,
        )

from __future__ import annotations

from bindai_core.context import ExecutionContext
from ..result import AgentResult
from bindai_core.events import (
    AgentStartedEvent,
    AgentFinishedEvent,
)

from .pipeline import ExecutionPipeline
from .state import ExecutionState

from .initialization_step import InitializationStep
from .knowledge_step import KnowledgeStep
from .memory_step import MemoryStep
from .model_generation_step import ModelGenerationStep
from .finish_step import FinishStep

from .tool_execution_step import ToolExecutionStep


class AgentExecutionEngine:
    """
    Pipeline execution engine.
    """

    def __init__(
        self,
        agent,
    ):
        self.agent = agent

        self.pipeline = ExecutionPipeline()

        self.pipeline.add(
            InitializationStep(),
        )

        self.pipeline.add(
            KnowledgeStep(),
        )

        self.pipeline.add(
            MemoryStep(),
        )

        self.pipeline.add(
            ModelGenerationStep(),
        )

        self.pipeline.add(
            ToolExecutionStep(),
        )

        self.pipeline.add(
            FinishStep(),
        )

    def execute(
        self,
        agent,
        context: ExecutionContext,
    ) -> AgentResult:

        context.data = context.data or ExecutionState()

        #
        # Agent started
        #

        agent.events.publish(
            AgentStartedEvent(),
        )

        #
        # before middleware
        #

        for middleware in agent.middleware:
            middleware.before_execute(
                agent,
                context,
            )

        #
        # run pipeline
        #

        result: AgentResult = self.pipeline.execute(
            agent,
            context,
        )

        #
        # after middleware
        #

        for middleware in reversed(agent.middleware):
            middleware.after_execute(
                agent,
                context,
                result,
            )

        #
        # Agent finished
        #

        agent.events.publish(
            AgentFinishedEvent(),
        )

        return result

    def stream(
        self,
        agent,
        context,
    ):
        """
        Stream tokens directly from the provider.
        """

        #
        # initialize execution state
        #

        context.data = ExecutionState(
            streaming=True,
        )

        InitializationStep().execute(
            agent,
            context,
        )

        state = context.data

        #
        # optional knowledge
        #

        KnowledgeStep().execute(
            agent,
            context,
        )

        #
        # optional memory
        #

        MemoryStep().execute(
            agent,
            context,
        )

        #
        # stream directly from provider
        #

        return agent.provider.stream(
            state.request,
        )
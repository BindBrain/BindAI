from __future__ import annotations

from bindai_core.context import ExecutionContext

from .pipeline import ExecutionPipeline
from .state import ExecutionState

from .initialization_step import InitializationStep
from .knowledge_step import KnowledgeStep
from .memory_step import MemoryStep
from .model_generation_step import ModelGenerationStep
from .finish_step import FinishStep


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
            FinishStep(),
        )

    def execute(
        self,
        agent,
        context: ExecutionContext,
    ):

        context.data = ExecutionState()

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

        result = self.pipeline.execute(
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

        return result

    def stream(
        self,
        agent,
        context: ExecutionContext,
    ):
        raise NotImplementedError("Streaming not implemented.")

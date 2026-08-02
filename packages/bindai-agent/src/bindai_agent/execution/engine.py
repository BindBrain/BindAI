from __future__ import annotations

from bindai_core.context import ExecutionContext
from bindai_core.events import (
    AgentFinishedEvent,
    AgentStartedEvent,
)

from ..result import AgentResult
from .finish_step import FinishStep
from .initialization_step import InitializationStep
from .knowledge_step import KnowledgeStep
from .memory_step import MemoryStep
from .model_generation_step import ModelGenerationStep
from .model_stream_step import ModelStreamStep
from .pipeline_builder import PipelineBuilder
from .state import ExecutionState
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

        self.pipeline = (
            PipelineBuilder()
            .add(InitializationStep())
            .add(KnowledgeStep())
            .add(MemoryStep())
            .add(ModelGenerationStep())
            .add(ToolExecutionStep())
            .add(FinishStep())
            .build()
        )

        self.streaming_pipeline = (
            PipelineBuilder()
            .add(InitializationStep())
            .add(KnowledgeStep())
            .add(MemoryStep())
            .add(ModelStreamStep())
            .build()
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

        try:
            #
            # Lifecycle
            #

            agent.before_run(
                context,
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

            agent.after_run(
                context,
                result,
            )

            return result

        except Exception as ex:
            agent.on_error(
                context,
                ex,
            )

            raise

        finally:
            #
            # Agent finished
            #

            agent.events.publish(
                AgentFinishedEvent(),
            )

    def stream(
        self,
        agent,
        context,
    ):
        """
        Stream tokens directly from the provider.
        """

        context.data = ExecutionState(
            streaming=True,
        )

        agent.events.publish(
            AgentStartedEvent(),
        )

        agent.before_run(
            context,
        )

        try:
            return self.streaming_pipeline.execute(
                agent,
                context,
            )

        except Exception as ex:
            agent.on_error(
                context,
                ex,
            )

            raise

        finally:
            agent.events.publish(
                AgentFinishedEvent(),
            )

from __future__ import annotations

from typing import cast

from bindai_core.context import ExecutionContext
from bindai_core.events import (
    AgentFinishedEvent,
    AgentStartedEvent,
)

from ..result import AgentResult
from ..nodes import NodeExecutionStep
from ..nodes import AgentNode
from .finish_step import FinishStep
from .initialization_step import InitializationStep
from .knowledge_step import KnowledgeStep
from .memory_step import MemoryStep
from .model_generation_step import ModelGenerationStep
from .model_stream_step import ModelStreamStep
from .pipeline_builder import PipelineBuilder
from .state import ExecutionState
from .tool_execution_step import ToolExecutionStep
from .request_build_step import RequestBuildStep


class AgentExecutionEngine:
    """
    Pipeline execution engine.
    """

    def __init__(
        self,
        agent,
    ):
        self.agent = agent

        self.nodes = []

        self.nodes: list[AgentNode] = []

        self.pipeline = self._build_pipeline()

        self.streaming_pipeline = (
            PipelineBuilder()
            .add(InitializationStep())
            .add(KnowledgeStep())
            .add(MemoryStep())
            .add(ModelStreamStep())
            .build()
        )


    def add_node(
        self,
        node: AgentNode,
    ) -> None:

        self.nodes.append(
            node,
        )

        self.pipeline = self._build_pipeline()


    def _build_pipeline(self):

        builder = (
            PipelineBuilder()
            .add(InitializationStep())
            .add(KnowledgeStep())
            .add(MemoryStep())
            .add(RequestBuildStep())
        )


        for node in self.nodes:
            builder.add(
                NodeExecutionStep(node),
            )


        return (
            builder
            .add(ModelGenerationStep())
            .add(ToolExecutionStep())
            .add(FinishStep())
            .build()
        )


    def execute(
        self,
        agent,
        context: ExecutionContext,
    ) -> AgentResult:

        context.data = context.data or ExecutionState()

        agent.events.publish(
            AgentStartedEvent(),
        )

        try:

            agent.before_run(
                context,
            )

            for middleware in agent.middleware:

                middleware.before_execute(
                    agent,
                    context,
                )

            #
            # Studio graph
            #

            from ..studio.execution import (
                StudioNodeExecutionStep,
            )

            if (
                self.nodes
                and isinstance(
                    self.nodes[0],
                    StudioNodeExecutionStep,
                )
            ):

                for node_step in self.nodes:

                    node_step.execute(
                        agent,
                        context,
                    )

                studio_result = self.nodes[0].result

                for middleware in reversed(
                    agent.middleware
                ):

                    middleware.after_execute(
                        agent,
                        context,
                        studio_result,
                    )

                agent.after_run(
                    context,
                    studio_result,
                )

                return studio_result

            #
            # Ordinary manually-added nodes
            #

            if self.nodes:

                for node_step in self.nodes:

                    node_result = node_step.execute(
                        agent,
                        context,
                    )

                    if node_result is not None:

                        return node_result

            #
            # Standard agent pipeline
            #

            result = cast(
                AgentResult,
                self.pipeline.execute(
                    agent,
                    context,
                ),
            )

            for middleware in reversed(
                agent.middleware
            ):

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

            if (
                self.nodes
                and isinstance(
                    self.nodes[0],
                    StudioNodeExecutionStep,
                )
            ):

                studio_result = self.nodes[0].result

                if studio_result is not None:

                    agent.on_error(
                        context,
                        ex,
                    )

                    return studio_result

            agent.on_error(
                context,
                ex,
            )

            raise

        finally:

            agent.events.publish(
                AgentFinishedEvent(),
            )

    def stream(
        self,
        agent,
        context,
    ):

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

            from ..studio.execution import (
                StudioNodeExecutionStep,
            )

            if (
                self.nodes
                and isinstance(
                    self.nodes[0],
                    StudioNodeExecutionStep,
                )
            ):

                studio_result = self.nodes[0].result

                if studio_result is not None:

                    agent.on_error(
                        context,
                        ex,
                    )

                    return studio_result

            agent.on_error(
                context,
                ex,
            )

            raise

        finally:

            agent.events.publish(
                AgentFinishedEvent(),
            )

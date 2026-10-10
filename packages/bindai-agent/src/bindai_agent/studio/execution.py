from __future__ import annotations

from bindai_agent.nodes import NodeExecutionStep

from .runtime import (
    apply_inputs,
    store_output,
)
from .result import StudioExecutionResult


class StudioNodeExecutionStep(
    NodeExecutionStep,
):

    def __init__(
        self,
        node,
        node_id: str,
        config: dict,
        graph=None,
        result: StudioExecutionResult | None = None,
    ):
        super().__init__(
            node,
        )

        self.node_id = node_id
        self.config = config
        self.graph = graph
        self.result = result


    def execute(
        self,
        agent,
        context,
    ):

        context.variables.set(
            "studio_node_id",
            self.node_id,
        )

        context.variables.set(
            "studio_node_config",
            self.config,
        )

        try:

            if self.graph is not None:

                apply_inputs(
                    self.graph,
                    self.node_id,
                    context,
                )

            result = super().execute(
                agent,
                context,
            )

            store_output(
                self.node_id,
                result,
                context,
            )

            if self.result is not None:

                self.result.set_output(
                    self.node_id,
                    result,
                )

            return result

        except Exception as ex:

            if self.result is not None:

                self.result.fail(
                    self.node_id,
                    ex,
                )

            raise

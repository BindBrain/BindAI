from __future__ import annotations

import yaml
from bindai_agent import AgentRegistry
from bindai_workflow import WorkflowBuilder
from bindai_workflow.nodes.agent import AgentNode
from bindai_workflow.nodes.end import EndNode
from bindai_workflow.nodes.start import StartNode

from .models import (
    WorkflowConfig,
    WorkflowEdgeConfig,
    WorkflowNodeConfig,
)


class WorkflowLoader:
    def load(
        self,
        path: str,
    ):

        with open(
            path,
            encoding="utf8",
        ) as f:
            data = yaml.safe_load(f)

        config = self._parse(
            data,
        )

        return self._build(
            config,
        )

    #
    # Parsing
    #

    def _parse(
        self,
        data,
    ) -> WorkflowConfig:

        workflow = data["workflow"]

        config = WorkflowConfig(
            name=workflow.get(
                "name",
                "workflow",
            ),
        )

        for item in workflow.get(
            "nodes",
            [],
        ):
            config.nodes.append(
                WorkflowNodeConfig(
                    id=item["id"],
                    type=item["type"],
                    agent=item.get("agent"),
                    tool=item.get("tool"),
                    input_variable=item.get(
                        "input_variable",
                        "input",
                    ),
                    output_variable=item.get(
                        "output_variable",
                        "output",
                    ),
                )
            )

        for item in workflow.get(
            "edges",
            [],
        ):
            config.edges.append(
                WorkflowEdgeConfig(
                    source=item["from"],
                    target=item["to"],
                )
            )

        return config

    #
    # Runtime
    #

    def _build(
        self,
        config: WorkflowConfig,
    ):

        builder = WorkflowBuilder(
            config.name,
        )

        nodes = {}

        from typing import Any

        for item in config.nodes:
            node: Any
            if item.type == "start":
                node = StartNode(item.id)

            elif item.type == "end":
                node = EndNode(item.id)

            elif item.type == "agent":

                if item.agent is None:
                    raise ValueError(
                        f"Agent node '{item.id}' is missing an agent."
                    )

                AgentRegistry.get(item.agent)

                node = AgentNode(
                    node_id=item.id,
                    agent=item.agent,
                    input_variable=item.input_variable,
                    output_variable=item.output_variable,
                )

            else:
                raise ValueError(f"Unknown workflow node '{item.type}'.")

            nodes[item.id] = node

            builder.add(node)

        workflow = builder.build()

        #
        # edges next
        #

        return workflow

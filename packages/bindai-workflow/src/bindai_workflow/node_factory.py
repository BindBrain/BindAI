from __future__ import annotations

from collections.abc import Callable
from typing import Any

from bindai_agent.registry import AgentRegistry
from bindai_tool.registry import ToolRegistry

from .node import WorkflowNode
from .nodes.agent import AgentNode
from .nodes.condition import ConditionNode
from .nodes.decision import DecisionNode
from .nodes.end import EndNode
from .nodes.human import HumanTaskNode
from .nodes.join import JoinNode
from .nodes.loop import LoopNode
from .nodes.parallel import ParallelNode
from .nodes.start import StartNode
from .nodes.subworkflow import SubWorkflowNode
from .nodes.tool import ToolNode


class WorkflowNodeFactory:
    """
    Creates workflow nodes from serialized definitions.

    Runtime dependencies are resolved through existing BindAI
    registries rather than being recreated by the workflow package.
    """

    def __init__(
        self,
        *,
        tool_registry: ToolRegistry | None = None,
        callable_resolver: Callable[[dict[str, Any]], Callable] | None = None,
    ):
        self._types: dict[
            str,
            type[WorkflowNode],
        ] = {}

        self.tool_registry = tool_registry
        self.callable_resolver = callable_resolver

        self.register(StartNode)
        self.register(EndNode)
        self.register(AgentNode)
        self.register(ToolNode)
        self.register(ConditionNode)
        self.register(DecisionNode)
        self.register(ParallelNode)
        self.register(JoinNode)
        self.register(LoopNode)
        self.register(HumanTaskNode)
        self.register(SubWorkflowNode)

    def register(
        self,
        node_type: type[WorkflowNode],
    ) -> None:

        self._types[node_type.__name__] = node_type

    def create(
        self,
        data: dict,
    ) -> WorkflowNode:

        node_type = data["type"]

        if node_type not in self._types:
            raise ValueError(
                f"Unknown workflow node type: {node_type}"
            )

        node_class = self._types[node_type]

        if node_class is AgentNode:
            node = self._create_agent(data)

        elif node_class is ToolNode:
            node = self._create_tool(data)

        elif node_class is ConditionNode:
            node = self._create_condition(data)

        elif node_class is DecisionNode:
            node = DecisionNode(
                node_id=data["id"],
                expression=data["expression"],
                name=data.get("name"),
            )

        elif node_class is JoinNode:
            node = JoinNode(
                node_id=data["id"],
                expected=data["expected"],
                name=data.get("name"),
            )

        elif node_class is LoopNode:
            node = self._create_loop(data)

        elif node_class is HumanTaskNode:
            node = HumanTaskNode(
                node_id=data["id"],
                assignee=data.get("assignee"),
                form=data.get("form"),
                name=data.get("name"),
            )

        elif node_class is SubWorkflowNode:
            node = SubWorkflowNode(
                node_id=data["id"],
                workflow_id=data["workflow_id"],
                name=data.get("name"),
            )

        else:
            node = node_class(
                node_id=data["id"],
                name=data.get("name"),
            )

        node.load_dict(
            data,
        )

        return node

    def _create_agent(
        self,
        data: dict,
    ) -> AgentNode:

        agent_name = data["agent"]

        if not AgentRegistry.contains(agent_name):
            raise ValueError(
                f"Agent '{agent_name}' is not registered."
            )

        return AgentNode(
            node_id=data["id"],
            agent=agent_name,
            input_variable=data.get(
                "input_variable",
                "input",
            ),
            output_variable=data.get(
                "output_variable",
                "agent_output",
            ),
            input_mapping=data.get(
                "input_mapping",
                {},
            ),
            name=data.get("name"),
        )

    def _create_tool(
        self,
        data: dict,
    ) -> ToolNode:

        if self.tool_registry is None:
            raise ValueError(
                "A ToolRegistry is required to deserialize ToolNode."
            )

        tool_name = data["tool"]

        if not self.tool_registry.contains(tool_name):
            raise ValueError(
                f"Tool '{tool_name}' is not registered."
            )

        return ToolNode(
            node_id=data["id"],
            tool=self.tool_registry.get(tool_name),
            output_variable=data.get(
                "output_variable",
                "tool_output",
            ),
            parameter_mapping=data.get(
                "parameter_mapping",
                {},
            ),
            name=data.get("name"),
        )

    def _create_condition(
        self,
        data: dict,
    ) -> ConditionNode:

        if self.callable_resolver is None:
            raise ValueError(
                "ConditionNode requires a callable_resolver "
                "when deserializing a workflow."
            )

        predicate = self.callable_resolver(
            data,
        )

        return ConditionNode(
            node_id=data["id"],
            predicate=predicate,
        )

    def _create_loop(
        self,
        data: dict,
    ) -> LoopNode:

        expression = data.get(
            "expression",
        )

        if expression:
            return LoopNode(
                node_id=data["id"],
                expression=str(expression),
                name=data.get("name"),
            )

        if self.callable_resolver is None:
            raise ValueError(
                "LoopNode requires either an expression "
                "or a callable_resolver when deserializing "
                "a workflow."
            )

        predicate = self.callable_resolver(
            data,
        )

        return LoopNode(
            node_id=data["id"],
            predicate=predicate,
            name=data.get("name"),
        )

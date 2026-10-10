from __future__ import annotations

from collections.abc import Callable
from typing import Any

from bindai_agent.registry import AgentRegistry

from ..nodes.agent import AgentNode
from ..nodes.condition import ConditionNode
from ..nodes.decision import DecisionNode
from ..nodes.end import EndNode
from ..nodes.human import HumanTaskNode
from ..nodes.join import JoinNode
from ..nodes.loop import LoopNode
from ..nodes.parallel import ParallelNode
from ..nodes.start import StartNode
from ..nodes.subworkflow import SubWorkflowNode
from ..nodes.tool import ToolNode
from ..workflow import Workflow
from ..store import WorkflowStore
from .models import WorkflowDefinition, WorkflowNodeDefinition


class WorkflowDefinitionRuntime:
    def __init__(
        self,
        *,
        tool_registry: Any | None = None,
        callable_resolver: Callable[[WorkflowNodeDefinition], Callable]
        | None = None,
        store: WorkflowStore | None = None,
    ) -> None:
        self.tool_registry = tool_registry
        self.callable_resolver = callable_resolver
        self.store = store

    def build(self, definition: WorkflowDefinition) -> Workflow:
        workflow = Workflow(
            name=definition.name,
            store=self.store,
        )
        workflow.id = definition.id
        workflow.version = definition.version

        for node_definition in definition.nodes:
            node = self._create_node(node_definition)
            workflow.add_node(node)

        self._connect(workflow, definition)

        return workflow

    def _create_node(self, definition: WorkflowNodeDefinition):
        node_type = definition.type.strip().lower()
        config = definition.configuration

        if node_type in {"start", "startnode"}:
            return StartNode(definition.id)

        if node_type in {"end", "endnode"}:
            return EndNode(definition.id)

        if node_type in {"agent", "agentnode"}:
            agent_name = config.get("agent")

            if not agent_name:
                raise ValueError(
                    f"Agent node '{definition.id}' is missing 'agent'."
                )

            if not AgentRegistry.contains(agent_name):
                raise ValueError(
                    f"Agent '{agent_name}' is not registered."
                )

            return AgentNode(
                node_id=definition.id,
                agent=agent_name,
                input_variable=config.get(
                    "input_variable",
                    "input",
                ),
                output_variable=config.get(
                    "output_variable",
                    "output",
                ),
            )

        if node_type in {"tool", "toolnode"}:
            tool_name = config.get("tool")

            if not tool_name:
                raise ValueError(
                    f"Tool node '{definition.id}' is missing 'tool'."
                )

            if self.tool_registry is None:
                raise ValueError(
                    "A tool registry is required to build tool nodes."
                )

            if not self.tool_registry.contains(tool_name):
                raise ValueError(
                    f"Tool '{tool_name}' is not registered."
                )

            tool = self.tool_registry.get(tool_name)

            return ToolNode(
                node_id=definition.id,
                tool=tool,
                output_variable=config.get(
                    "output_variable",
                    "tool_output",
                ),
                parameter_mapping=config.get(
                    "parameter_mapping",
                    {},
                ),
            )

        if node_type in {"decision", "decisionnode"}:
            expression = config.get("expression")

            if not expression:
                raise ValueError(
                    f"Decision node '{definition.id}' is missing "
                    "'expression'."
                )

            return DecisionNode(
                node_id=definition.id,
                expression=str(expression),
            )

        if node_type in {"condition", "conditionnode"}:
            expression = config.get("expression")

            if expression:
                return ConditionNode(
                    node_id=definition.id,
                    expression=str(expression),
                )

            if self.callable_resolver is None:
                raise ValueError(
                    "Condition node requires either an expression "
                    "or a callable resolver."
                )

            predicate = self.callable_resolver(definition)

            return ConditionNode(
                node_id=definition.id,
                predicate=predicate,
            )

        if node_type in {"parallel", "parallelnode"}:
            return ParallelNode(node_id=definition.id)

        if node_type in {"join", "joinnode"}:
            expected = config.get("expected")

            if expected is None:
                raise ValueError(
                    f"Join node '{definition.id}' is missing 'expected'."
                )

            return JoinNode(
                node_id=definition.id,
                expected=int(expected),
                name=definition.name,
            )

        if node_type in {"loop", "loopnode"}:
            expression = config.get("expression")

            if expression:
                return LoopNode(
                    node_id=definition.id,
                    expression=str(expression),
                    name=definition.name,
                )

            if self.callable_resolver is None:
                raise ValueError(
                    "Loop node requires either an expression "
                    "or a callable resolver."
                )

            predicate = self.callable_resolver(definition)

            return LoopNode(
                node_id=definition.id,
                predicate=predicate,
                name=definition.name,
            )

        if node_type in {
            "human_task",
            "humantask",
            "humantasknode",
        }:
            return HumanTaskNode(
                node_id=definition.id,
                assignee=config.get("assignee"),
                form=config.get("form"),
                name=definition.name,
            )

        if node_type in {
            "subworkflow",
            "subworkflownode",
        }:
            workflow_id = config.get("workflow_id")

            if not workflow_id:
                raise ValueError(
                    f"Subworkflow node '{definition.id}' is missing "
                    "'workflow_id'."
                )

            return SubWorkflowNode(
                node_id=definition.id,
                workflow_id=str(workflow_id),
                name=definition.name,
            )

        raise ValueError(
            f"Unsupported workflow node type '{definition.type}'."
        )

    def _connect(
        self,
        workflow: Workflow,
        definition: WorkflowDefinition,
    ) -> None:
        for node in workflow.nodes.values():
            node.next_nodes.clear()

            if isinstance(node, (DecisionNode, ConditionNode)):
                node.true_node = None
                node.false_node = None

            if isinstance(node, HumanTaskNode):
                node.approved_node = None
                node.rejected_node = None

        for edge in definition.edges:
            source = workflow.get(edge.source)
            target = workflow.get(edge.target)

            if isinstance(source, (DecisionNode, ConditionNode)):
                self._connect_branch(
                    source,
                    target.id,
                    edge.port,
                )
                continue

            if isinstance(source, HumanTaskNode):
                self._connect_human_task(
                    source,
                    target.id,
                    edge.port,
                )
                continue

            if isinstance(source, LoopNode):
                self._connect_loop(
                    source,
                    target.id,
                    edge.port,
                )
                continue

            source.next_nodes.append(target.id)

        start_nodes = [
            node
            for node in definition.nodes
            if node.type.strip().lower()
            in {"start", "startnode"}
        ]

        if not start_nodes:
            raise ValueError(
                "Workflow definition does not contain a start node."
            )

        if len(start_nodes) > 1:
            raise ValueError(
                "Workflow definition contains multiple start nodes."
            )

        workflow.start_node = start_nodes[0].id

    @staticmethod
    def _connect_branch(
        source: DecisionNode | ConditionNode,
        target_id: str,
        port: str | None,
    ) -> None:
        if port not in {"true", "false"}:
            raise ValueError(
                f"Node '{source.id}' requires edge port "
                "'true' or 'false'."
            )

        if port == "true":
            if source.true_node is not None:
                raise ValueError(
                    f"Node '{source.id}' has multiple true branches."
                )

            source.true_node = target_id
            return

        if source.false_node is not None:
            raise ValueError(
                f"Node '{source.id}' has multiple false branches."
            )

        source.false_node = target_id

    @staticmethod
    def _connect_human_task(
        source: HumanTaskNode,
        target_id: str,
        port: str | None,
    ) -> None:
        # Preserve compatibility with older linear human-task workflows.
        if port is None:
            source.next_nodes.append(target_id)
            return

        if port == "approved":
            if source.approved_node is not None:
                raise ValueError(
                    f"Human task node '{source.id}' has multiple "
                    "approved branches."
                )

            source.approved_node = target_id
            return

        if port == "rejected":
            if source.rejected_node is not None:
                raise ValueError(
                    f"Human task node '{source.id}' has multiple "
                    "rejected branches."
                )

            source.rejected_node = target_id
            return

        raise ValueError(
            f"Human task node '{source.id}' has unsupported edge port "
            f"'{port}'. Expected 'approved' or 'rejected'."
        )

    @staticmethod
    def _connect_loop(
        source: LoopNode,
        target_id: str,
        port: str | None,
    ) -> None:
        if port not in {"body", "exit"}:
            raise ValueError(
                f"Loop node '{source.id}' requires edge port "
                "'body' or 'exit'."
            )

        while len(source.next_nodes) < 2:
            source.next_nodes.append(None)

        index = 0 if port == "body" else 1

        existing = source.next_nodes[index]

        if existing is not None and existing != target_id:
            branch = "body" if index == 0 else "exit"
            raise ValueError(
                f"Loop node '{source.id}' has multiple "
                f"{branch} branches."
            )

        source.next_nodes[index] = target_id

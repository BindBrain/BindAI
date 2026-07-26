from __future__ import annotations

from .workflow import Workflow
from .node import WorkflowNode
from .validation import WorkflowValidator

from .nodes.agent import AgentNode
from .nodes.start import StartNode
from .nodes.end import EndNode

from .nodes.condition import ConditionNode
from .nodes.parallel import ParallelNode
from .nodes.loop import LoopNode

from typing import Callable

from .nodes.condition import ConditionNode
from .nodes.parallel import ParallelNode
from .nodes.loop import LoopNode

class WorkflowBuilder:

    def __init__(
        self,
        name: str | None = None,
    ):

        self._workflow = Workflow(name)

        self._last: WorkflowNode | None = None

    def start(
        self,
        node: WorkflowNode,
    ):

        self._workflow.add_node(node)

        self._workflow.start_node = node.id

        self._last = node

        return self

    def then(
        self,
        node: WorkflowNode,
    ):

        if self._last is None:
            raise RuntimeError(
                "Workflow has no start node.",
            )

        self._workflow.add_node(node)

        self._last.next_nodes.append(
            node.id,
        )

        self._last = node

        return self

    def add(
        self,
        node: WorkflowNode,
    ):

        self._workflow.add_node(node)

        return self

    def build(
        self,
    ) -> Workflow:

        validator = WorkflowValidator()

        errors = validator.validate(
            self._workflow,
        )

        if errors:
            raise ValueError(
                "\n".join(errors),
            )

        return self._workflow

    def agent(
        self,
        agent,
        *,
        input_variable: str = "input",
        output_variable: str = "agent_output",
    ):

        self._workflow.agents[agent.name] = agent

        node = AgentNode(
            node_id=agent.name,
            agent=agent.name,
            input_variable=input_variable,
            output_variable=output_variable,
        )

        if self._last is None:
            return self.start(node)

        return self.then(node)

    def start_node(
        self,
    ):

        return self.start(
            StartNode("start"),
        )

    def end_node(
        self,
    ):

        return self.then(
            EndNode("end"),
        )

    def condition(
        self,
        expression: str,
    ):

        node = ConditionNode(
            node_id=f"condition_{len(self._workflow.nodes)}",
            expression=expression,
        )

        return self.then(node)

    def parallel(
        self,
    ):

        node = ParallelNode(
            node_id=f"parallel_{len(self._workflow.nodes)}",
        )

        return self.then(node)

    def loop(
        self,
        expression: str,
    ):

        node = LoopNode(
            node_id=f"loop_{len(self._workflow.nodes)}",
            expression=expression,
        )

        return self.then(node)

    def condition(
        self,
        predicate: Callable,
    ):

        node = ConditionNode(
            node_id=f"condition_{len(self._workflow.nodes)}",
            predicate=predicate,
        )

        return self.then(
            node,
        )


    def parallel(
        self,
    ):

        node = ParallelNode(
            node_id=f"parallel_{len(self._workflow.nodes)}",
        )

        return self.then(
            node,
        )


    def loop(
        self,
        predicate: Callable,
    ):

        node = LoopNode(
            node_id=f"loop_{len(self._workflow.nodes)}",
            predicate=predicate,
        )

        return self.then(
            node,
        )
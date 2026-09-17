from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from bindai_agent.registry import AgentRegistry
from bindai_tool import Tool

from .node import WorkflowNode
from .nodes.agent import AgentNode
from .nodes.condition import ConditionNode
from .nodes.end import EndNode
from .nodes.human import HumanTaskNode
from .nodes.join import JoinNode
from .nodes.loop import LoopNode
from .nodes.parallel import ParallelNode
from .nodes.start import StartNode
from .nodes.subworkflow import SubWorkflowNode
from .nodes.tool import ToolNode
from .validation import WorkflowValidator
from .workflow import Workflow

if TYPE_CHECKING:
    from bindai_agent import Agent


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
        agent: Agent,
        *,
        input_variable: str = "input",
        output_variable: str = "agent_output",
    ):

        self._workflow.agents[agent.name] = agent

        AgentRegistry.register(agent)

        node = AgentNode(
            node_id=agent.name,
            agent=agent.name,
            input_variable=input_variable,
            output_variable=output_variable,
        )

        if self._last is None:
            return self.start(node)

        return self.then(node)

    def tool(
        self,
        tool: Tool,
        *,
        output_variable: str = "tool_output",
    ):

        node = ToolNode(
            node_id=tool.name,
            tool=tool,
            output_variable=output_variable,
        )

        if self._last is None:
            return self.start(node)

        return self.then(node)

    def human_task(
        self,
        assignee: str | None = None,
        form: str | None = None,
        *,
        node_id: str | None = None,
        name: str | None = None,
    ):

        node = HumanTaskNode(
            node_id=node_id or f"human_task_{len(self._workflow.nodes)}",
            assignee=assignee,
            form=form,
            name=name,
        )

        if self._last is None:
            return self.start(node)

        return self.then(node)

    def subworkflow(
        self,
        workflow_id: str,
        *,
        node_id: str | None = None,
        name: str | None = None,
    ):

        node = SubWorkflowNode(
            node_id=node_id or f"subworkflow_{len(self._workflow.nodes)}",
            workflow_id=workflow_id,
            name=name,
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
        predicate: Callable,
        *,
        when_true: WorkflowNode | None = None,
        when_false: WorkflowNode | None = None,
    ):

        node = ConditionNode(
            node_id=f"condition_{len(self._workflow.nodes)}",
            predicate=predicate,
        )

        if self._last is None:
            self.start(node)
        else:
            self.then(node)

        if when_true is not None:
            self._workflow.add_node(
                when_true,
            )
            node.when_true(
                when_true,
            )

        if when_false is not None:
            self._workflow.add_node(
                when_false,
            )
            node.when_false(
                when_false,
            )

        return self

    def parallel(
        self,
        *branches: WorkflowNode,
    ):
        node = ParallelNode(
            node_id=f"parallel_{len(self._workflow.nodes)}",
        )

        if self._last is None:
            self.start(node)
        else:
            self.then(node)

        for branch in branches:
            self._workflow.add_node(branch)
            node.next_nodes.append(branch.id)

        return self

    def join(
        self,
        expected: int | None = None,
        *,
        node_id: str | None = None,
        name: str | None = None,
    ):
        if self._last is None:
            raise RuntimeError(
                "Workflow has no parallel node.",
            )

        parallel = self._last

        if not isinstance(parallel, ParallelNode):
            raise RuntimeError(
                "Join must follow a parallel node.",
            )

        if not parallel.next_nodes:
            raise RuntimeError(
                "Parallel node has no branches.",
            )

        join = JoinNode(
            node_id=node_id or f"join_{len(self._workflow.nodes)}",
            expected=expected or len(parallel.next_nodes),
            name=name,
        )

        self._workflow.add_node(join)

        for branch_id in parallel.next_nodes:
            branch = self._workflow.get(branch_id)
            branch.next_nodes.append(join.id)

        self._last = join

        return self

    def loop(
        self,
        predicate: Callable,
        *,
        body: WorkflowNode,
        exit: WorkflowNode,
    ):
        node = LoopNode(
            node_id=f"loop_{len(self._workflow.nodes)}",
            predicate=predicate,
        )

        if self._last is None:
            self.start(node)
        else:
            self.then(node)

        self._workflow.add_node(body)
        self._workflow.add_node(exit)

        node.next_nodes = [
            body.id,
            exit.id,
        ]

        body.next_nodes.append(
            node.id,
        )

        self._last = exit

        return self

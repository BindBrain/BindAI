from __future__ import annotations

from typing import TYPE_CHECKING

from bindai_agent import AgentRegistry

from .runnable import RunnableNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


class AgentNode(
    RunnableNode,
):
    def __init__(
        self,
        node_id: str,
        agent: str,
        input_variable: str = "input",
        output_variable: str = "agent_output",
        input_mapping: dict[str, str] | None = None,
        name: str | None = None,
    ):
        super().__init__(
            node_id=node_id,
            runnable=AgentRegistry.get(agent),
            name=name,
        )

        self.agent = agent
        self.input_variable = input_variable
        self.output_variable = output_variable

        if isinstance(input_mapping, str):
            mapping = {}

            for line in input_mapping.splitlines():
                line = line.strip()

                if not line or "=" not in line:
                    continue

                name, variable = line.split("=", 1)

                name = name.strip()
                variable = variable.strip()

                if name and variable:
                    mapping[name] = variable

            self.input_mapping = mapping
        else:
            self.input_mapping = input_mapping or {}

    def before_execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:

        if hasattr(self.runnable, "conversation"):
            self.runnable.conversation.clear()

        if self.input_mapping:
            sections = []

            for name, variable in self.input_mapping.items():
                value = context.get(variable)

                if (
                    hasattr(value, "value")
                    and hasattr(value, "success")
                ):
                    value = value.value

                sections.append(
                    f"{name}:\n{value}"
                )

            prompt = "\n\n".join(sections)
        else:
            prompt = context.get(
                self.input_variable,
            )

        context.variables.set(
            "input",
            prompt,
        )

        return context

    def after_execute(
        self,
        context: WorkflowContext,
        result: object,
    ) -> WorkflowContext:

        context.set(
            self.output_variable,
            result.output,
        )

        return context

    def to_dict(
        self,
    ) -> dict:

        data = super().to_dict()

        data.update(
            {
                "agent": self.agent,
                "input_variable": self.input_variable,
                "output_variable": self.output_variable,
            }
        )

        if self.input_mapping:
            data["input_mapping"] = dict(
                self.input_mapping,
            )

        return data

    def load_dict(
        self,
        data: dict,
    ) -> None:

        super().load_dict(
            data,
        )

        self.agent = data["agent"]

        self.input_variable = data.get(
            "input_variable",
            "input",
        )

        self.output_variable = data.get(
            "output_variable",
            "agent_output",
        )

        self.input_mapping = dict(
            data.get(
                "input_mapping",
                {},
            ) or {},
        )

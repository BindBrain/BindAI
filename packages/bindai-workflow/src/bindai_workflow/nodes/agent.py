from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bindai_agent import AgentRegistry
from bindai_agent.result import AgentResult

from .runnable import RunnableNode

if TYPE_CHECKING:
    from ..context import WorkflowContext


class AgentNode(RunnableNode):
    def __init__(
        self,
        node_id: str,
        agent: str,
        input_variable: str = "input",
        output_variable: str = "agent_output",
        input_mapping: dict[str, str] | str | None = None,
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

        mapping: dict[str, str] = {}

        if isinstance(input_mapping, str):
            for line in input_mapping.splitlines():
                line = line.strip()

                if not line or "=" not in line:
                    continue

                key, variable = line.split("=", 1)
                key = key.strip()
                variable = variable.strip()

                if key and variable:
                    mapping[key] = variable
        elif input_mapping is not None:
            mapping = dict(input_mapping)

        self.input_mapping: dict[str, str] = mapping

    def before_execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:
        if hasattr(self.runnable, "conversation"):
            self.runnable.conversation.clear()

        if self.input_mapping:
            sections: list[str] = []

            for name, variable in self.input_mapping.items():
                value: object = context.get(variable)

                if hasattr(value, "value") and hasattr(value, "success"):
                    value = value.value

                sections.append(f"{name}:\n{value}")

            prompt = "\n\n".join(sections)
        else:
            prompt = str(context.get(self.input_variable, ""))

        context.variables.set("input", prompt)
        return context

    def after_execute(
        self,
        context: WorkflowContext,
        result: AgentResult,
    ) -> WorkflowContext:
        context.set(self.output_variable, result.output)
        return context

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()

        data.update(
            {
                "agent": self.agent,
                "input_variable": self.input_variable,
                "output_variable": self.output_variable,
            }
        )

        if self.input_mapping:
            data["input_mapping"] = dict(self.input_mapping)

        return data

    def load_dict(
        self,
        data: dict[str, Any],
    ) -> None:
        super().load_dict(data)

        self.agent = str(data["agent"])
        self.input_variable = str(data.get("input_variable", "input"))
        self.output_variable = str(data.get("output_variable", "agent_output"))

        raw_mapping = data.get("input_mapping", {})
        if isinstance(raw_mapping, dict):
            self.input_mapping = {str(key): str(value) for key, value in raw_mapping.items()}
        elif isinstance(raw_mapping, str):
            mapping: dict[str, str] = {}
            for line in raw_mapping.splitlines():
                line = line.strip()
                if not line or "=" not in line:
                    continue
                key, variable = line.split("=", 1)
                key = key.strip()
                variable = variable.strip()
                if key and variable:
                    mapping[key] = variable
            self.input_mapping = mapping
        else:
            self.input_mapping = {}

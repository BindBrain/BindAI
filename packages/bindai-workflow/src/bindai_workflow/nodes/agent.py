from __future__ import annotations

from .runnable import RunnableNode
from bindai_agent import AgentRegistry


class AgentNode(
    RunnableNode,
):
    def __init__(
        self,
        node_id: str,
        agent: str,
        input_variable: str = "input",
        output_variable: str = "agent_output",
        name: str | None = None,
    ):

        super().__init__(
            node_id=node_id,
            runnable=AgentRegistry.get(
                agent,
            ),
            name=name,
        )

        self.agent = agent
        self.input_variable = input_variable
        self.output_variable = output_variable

    def before_execute(
        self,
        context,
    ):

        prompt = context.get(
            self.input_variable,
        )

        #
        # Temporary compatibility
        #

        context.input = prompt

        return context


    def after_execute(
        self,
        context,
        result,
    ):

        context.set(
            self.output_variable,
            result,
        )

        return context

    def to_dict(
        self,
    ):

        data = super().to_dict()

        data.update(
            {
                "agent": self.agent,
                "input_variable": self.input_variable,
                "output_variable": self.output_variable,
            }
        )

        return data

    def load_dict(
        self,
        data: dict,
    ):

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
"""
Example 30: Full AI Application

Production-style BindAI application.

Demonstrates:

- Agent creation
- Custom tools
- Custom memory
- Workflow execution
- Application structure
"""

from bindai import AgentBuilder
from bindai_workflow import WorkflowBuilder
from bindai_workflow.context import WorkflowContext
from bindai_workflow.node import WorkflowNode

# ---------------------------------------------------------
# Tool Layer
# ---------------------------------------------------------


def get_customer_profile(
    customer_id: str,
) -> dict:

    customers = {
        "001": {
            "name": "Alice",
            "plan": "Enterprise",
            "status": "active",
        },
        "002": {
            "name": "Bob",
            "plan": "Starter",
            "status": "trial",
        },
    }

    return customers.get(
        customer_id,
        {
            "name": "Unknown",
            "plan": "Unknown",
            "status": "unknown",
        },
    )


# ---------------------------------------------------------
# Memory Layer
# ---------------------------------------------------------


class Memory:
    def __init__(self):

        self.messages = []

    def add(
        self,
        role: str,
        content: str,
    ):

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    def history(self):

        return self.messages


memory = Memory()


# ---------------------------------------------------------
# Agent Layer
# ---------------------------------------------------------


agent = (
    AgentBuilder()
    .name("Business Assistant")
    .instructions(
        """
        You are a business AI assistant.

        Help users understand:

        - customers
        - plans
        - accounts

        Always provide clear answers.
        """
    )
    .tools(get_customer_profile)
    .build()
)


# ---------------------------------------------------------
# Workflow Node
# ---------------------------------------------------------


class FunctionNode(WorkflowNode):
    def __init__(
        self,
        node_id: str,
        function,
    ):

        super().__init__(node_id)

        self.function = function

    def execute(
        self,
        context: WorkflowContext,
    ) -> WorkflowContext:

        result = self.function(context)

        if isinstance(
            result,
            dict,
        ):
            for key, value in result.items():
                context.set(
                    key,
                    value,
                )

        return context


# ---------------------------------------------------------
# Workflow Task
# ---------------------------------------------------------


def analyze_customer(
    context,
):

    customer_id = context.get("customer_id")

    customer = get_customer_profile(customer_id)

    memory.add("user", f"Analyze customer {customer_id}")

    result = agent.chat(
        f"""
        Analyze this customer.

        Customer information:

        {customer}

        Provide:

        - customer summary
        - account status
        - recommended actions
        """
    )

    memory.add(
        "assistant",
        result.output,
    )

    return {
        "customer": customer,
        "analysis": result.output,
        "memory": memory.history(),
    }


# ---------------------------------------------------------
# Workflow Definition
# ---------------------------------------------------------


customer_analysis_node = FunctionNode(
    "analyze_customer",
    analyze_customer,
)


workflow = (
    WorkflowBuilder("customer-analysis")
    .start_node()
    .then(customer_analysis_node)
    .end_node()
    .build()
)


# ---------------------------------------------------------
# Application Entry
# ---------------------------------------------------------


def main():

    print("=" * 60)

    print("BindAI Full Application Example")

    print("=" * 60)

    instance = workflow.create_instance()

    instance.context.set(
        "customer_id",
        "001",
    )

    result = workflow.executor.execute(instance)

    print()

    print("Result:")

    print(result)

    print()

    print("Memory:")

    for message in memory.history():
        print(message)


if __name__ == "__main__":
    main()

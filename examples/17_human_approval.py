"""
17. Human Approval Workflow
"""

from bindai_core.executable import Executable, ExecutionResult
from bindai_workflow import Workflow
from bindai_workflow.nodes import (
    EndNode,
    RunnableNode,
    StartNode,
)


class CreateProposal(Executable):
    def execute(self, context):

        context.variables["proposal"] = "Deploy the new AI workflow to production environment."

        return ExecutionResult(
            success=True,
            output=context.variables,
        )


class HumanApproval(Executable):
    def execute(self, context):

        proposal = context.variables["proposal"]

        print("\nApproval required:")
        print(proposal)

        answer = input("\nApprove? (yes/no): ")

        context.variables["approved"] = answer.lower() == "yes"

        return ExecutionResult(
            success=True,
            output=context.variables,
        )


class Deploy(Executable):
    def execute(self, context):

        if context.variables["approved"]:
            status = "Deployment completed"

        else:
            status = "Deployment rejected"

        return ExecutionResult(
            success=True,
            output={"status": status},
        )


workflow = Workflow("human-approval-flow")


start = StartNode("start")


proposal = RunnableNode(
    "proposal",
    CreateProposal(),
)


approval = RunnableNode(
    "approval",
    HumanApproval(),
)


deploy = RunnableNode(
    "deploy",
    Deploy(),
)


end = EndNode("end")


for node in [
    start,
    proposal,
    approval,
    deploy,
    end,
]:
    workflow.add_node(node)


start.next_nodes.append(proposal.id)

proposal.next_nodes.append(approval.id)

approval.next_nodes.append(deploy.id)

deploy.next_nodes.append(end.id)


workflow.start_node = start.id


result = workflow.run()


print()
print(result)

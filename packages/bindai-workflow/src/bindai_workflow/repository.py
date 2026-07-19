from __future__ import annotations
from .workflow import Workflow
from datetime import datetime
from .deployment import WorkflowDeployment

class WorkflowRepository:
    """
    Stores workflow definitions.
    """

    def __init__(self):
        self._deployments = {}
        self._workflows: dict[
            str,
            Workflow,
        ] = {}

    def register(
        self,
        workflow: Workflow,
    ):

        self._workflows[
            workflow.id
        ] = workflow

        return workflow

    def get(
        self,
        workflow_id: str,
    ) -> Workflow:

        return self._workflows[
            workflow_id
        ]

    def exists(
        self,
        workflow_id: str,
    ) -> bool:

        return (
            workflow_id
            in self._workflows
        )

    def all(
        self,
    ) -> list[Workflow]:

        return list(
            self._workflows.values()
        )
    
    def workflow(
        self,
        name: str,
    ) -> Workflow:

        for workflow in self._workflows.values():

            if workflow.name == name:

                return workflow

        raise KeyError(
            name,
        )

    def latest(
        self,
        name: str,
    ) -> Workflow:

        versions = [

            workflow

            for workflow in self._workflows.values()

            if workflow.name == name

        ]

        return max(

            versions,

            key=lambda workflow: workflow.version,

        )

    def deploy(
        self,
        workflow: Workflow,
    ):

        self._deployments[
            workflow.name
        ] = WorkflowDeployment(

            workflow_name=workflow.name,

            version=workflow.version,

            deployed_at=datetime.utcnow(),

        )

        return workflow

    def deployed(
        self,
        name: str,
    ) -> Workflow:

        deployment = self._deployments[
            name
        ]

        versions = [

            workflow

            for workflow in self._workflows.values()

            if (
                workflow.name == name
                and workflow.version == deployment.version
            )

        ]

        return versions[0]

    def rollback(
        self,
        name: str,
        version: int,
    ):

        workflow = [

            item

            for item in self._workflows.values()

            if (
                item.name == name
                and item.version == version
            )

        ][0]

        self.deploy(
            workflow,
        )

        return workflow
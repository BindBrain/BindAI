from __future__ import annotations

from bindai_application import Application
from bindai_core.tool import ToolRegistry
from bindai_workflow import WorkflowRegistry
from bindai_workflow import WorkflowScheduler

from .configuration import ProjectConfiguration


class Project:
    """
    Represents one BindAI project.

    A project is the root container of a BindAI solution.
    It owns applications, shared tools, workflows,
    configuration, knowledge, secrets, and other
    project-wide resources.
    """

    def __init__(
        self,
        configuration: ProjectConfiguration,
    ):

        self.configuration = configuration

        #
        # Applications
        #

        self.applications: dict[str, Application] = {}

        #
        # Shared Tools
        #

        self.tools = ToolRegistry()

        #
        # Workflows
        #

        self.workflows = WorkflowRegistry

        self.scheduler = WorkflowScheduler()

        #
        # Future
        #

        self.knowledge: dict[str, object] = {}

        self.memories: dict[str, object] = {}

        self.secrets: dict[str, object] = {}

    @property
    def name(
        self,
    ) -> str:

        return self.configuration.name

    #
    # Applications
    #

    def add_application(
        self,
        application: Application,
    ):

        self.applications[application.name] = application

        return self

    def application(
        self,
        name: str,
    ) -> Application:

        return self.applications[name]

    #
    # Shared Tools
    #

    def add_tool(
        self,
        tool,
    ):

        self.tools.register(
            tool,
        )

        return self

    #
    # Workflows
    #

    def add_workflow(
        self,
        workflow,
    ):

        self.workflows.register(
            workflow,
        )

        return self

    def workflow(
        self,
        workflow_id: str,
    ):

        return self.workflows.get(
            workflow_id,
        )

    #
    # Execution
    #

    def run(
        self,
        *,
        application: str,
        agent: str,
        message: str,
    ):

        return self.application(
            application,
        ).run(
            agent=agent,
            message=message,
        )

    def stream(
        self,
        *,
        application: str,
        agent: str,
        message: str,
    ):

        return self.application(
            application,
        ).stream(
            agent=agent,
            message=message,
        )

    #
    # Python Helpers
    #

    def __contains__(
        self,
        name: str,
    ):

        return name in self.applications

    def __len__(
        self,
    ):

        return len(self.applications)

    def __iter__(
        self,
    ):

        return iter(self.applications.values())

    def add_schedule(
        self,
        schedule,
    ):

        self.scheduler.add(
            schedule,
        )

        return self

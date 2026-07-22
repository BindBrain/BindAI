from __future__ import annotations

from bindai_project import Project

from .configuration import HostConfiguration


class BindHost:
    """
    Root BindAI runtime.
    """

    def __init__(
        self,
        configuration: HostConfiguration,
    ):

        self.configuration = configuration

        self.projects = {}

    @property
    def name(
        self,
    ):

        return self.configuration.name

    #
    # Projects
    #

    def add_project(
        self,
        project: Project,
    ):

        self.projects[project.name] = project

        return self

    def project(
        self,
        name: str,
    ) -> Project:

        return self.projects[name]

    #
    # Execution
    #

    def run(
        self,
        *,
        project: str,
        application: str,
        agent: str,
        message: str,
    ):

        return self.project(
            project,
        ).run(
            application=application,
            agent=agent,
            message=message,
        )

    def stream(
        self,
        *,
        project: str,
        application: str,
        agent: str,
        message: str,
    ):

        return self.project(
            project,
        ).stream(
            application=application,
            agent=agent,
            message=message,
        )

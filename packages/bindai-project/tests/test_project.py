from unittest.mock import Mock

import pytest

from bindai_application import Application
from bindai_application.configuration import ApplicationConfiguration
from bindai_project import Project, ProjectBuilder, ProjectConfiguration
from bindai_workflow import Workflow, WorkflowRegistry


@pytest.fixture(autouse=True)
def clear_workflow_registry():
    WorkflowRegistry.clear()
    yield
    WorkflowRegistry.clear()


def make_project() -> Project:
    return Project(
        ProjectConfiguration(
            name="test-project",
        )
    )


def make_application(name: str = "test-app") -> Application:
    return Application(
        ApplicationConfiguration(
            name=name,
        )
    )


def test_project_initializes_with_configuration_and_empty_resources():
    project = make_project()

    assert project.name == "test-project"
    assert project.configuration.version == "1.0.0"
    assert project.configuration.description == ""

    assert project.applications == {}
    assert len(project.tools) == 0
    assert WorkflowRegistry.size() == 0
    assert project.knowledge == {}
    assert project.memories == {}
    assert project.secrets == {}


def test_add_application_registers_and_returns_project():
    project = make_project()
    application = make_application()

    result = project.add_application(application)

    assert result is project
    assert project.application("test-app") is application
    assert project.applications["test-app"] is application
    assert "test-app" in project
    assert len(project) == 1
    assert list(project) == [application]


def test_application_can_be_replaced_by_name():
    project = make_project()
    first = make_application()
    second = make_application()

    project.add_application(first)
    project.add_application(second)

    assert len(project) == 1
    assert project.application("test-app") is second


def test_project_run_delegates_to_application():
    project = make_project()
    application = Mock()
    application.name = "test-app"
    application.run.return_value = "run-result"

    project.add_application(application)

    result = project.run(
        application="test-app",
        agent="assistant",
        message="Hello",
    )

    assert result == "run-result"
    application.run.assert_called_once_with(
        agent="assistant",
        message="Hello",
    )


def test_project_stream_delegates_to_application():
    project = make_project()
    application = Mock()
    application.name = "test-app"
    application.stream.return_value = "stream-result"

    project.add_application(application)

    result = project.stream(
        application="test-app",
        agent="assistant",
        message="Hello",
    )

    assert result == "stream-result"
    application.stream.assert_called_once_with(
        agent="assistant",
        message="Hello",
    )


def test_add_tool_registers_tool_and_returns_project():
    project = make_project()

    def test_tool(value: str) -> str:
        return value

    result = project.add_tool(test_tool)

    assert result is project
    assert len(project.tools) == 1
    assert project.tools.get("test_tool").name == "test_tool"


def test_add_workflow_registers_workflow_and_returns_project():
    project = make_project()
    workflow = Workflow(name="test-workflow")

    result = project.add_workflow(workflow)

    assert result is project
    assert project.workflow(workflow.id) is workflow
    assert WorkflowRegistry.contains(workflow.id)


def test_project_builder_builds_project():
    project = ProjectBuilder("builder-project").build()

    assert isinstance(project, Project)
    assert project.name == "builder-project"


def test_project_builder_registers_application():
    application = make_application("builder-app")

    project = (
        ProjectBuilder("builder-project")
        .application(application)
        .build()
    )

    assert project.application("builder-app") is application
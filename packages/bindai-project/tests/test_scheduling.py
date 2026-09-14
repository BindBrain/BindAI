from datetime import UTC, datetime

from bindai_project import Project
from bindai_project.configuration import ProjectConfiguration
from bindai_workflow import WorkflowSchedule


def test_project_add_schedule_registers_schedule() -> None:
    project = Project(
        ProjectConfiguration(
            name="test-project",
        )
    )

    schedule = WorkflowSchedule(
        workflow_id="workflow-1",
        next_run=datetime.now(UTC),
    )

    result = project.add_schedule(
        schedule,
    )

    assert result is project
    assert project.scheduler.due() == [schedule]
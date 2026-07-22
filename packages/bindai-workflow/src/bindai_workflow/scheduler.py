from __future__ import annotations

from datetime import datetime, timedelta

from .schedule import WorkflowSchedule


class WorkflowScheduler:
    """
    Keeps workflow schedules.
    """

    def __init__(self):

        self._schedules: list[WorkflowSchedule] = []

    def add(
        self,
        schedule: WorkflowSchedule,
    ):

        self._schedules.append(
            schedule,
        )

    def due(
        self,
    ) -> list[WorkflowSchedule]:

        now = datetime.utcnow()

        due = []

        for schedule in self._schedules:
            if schedule.enabled and schedule.next_run <= now:
                due.append(
                    schedule,
                )

        return due

    def reschedule(
        self,
        schedule: WorkflowSchedule,
    ):

        if schedule.interval_seconds:
            schedule.next_run += timedelta(
                seconds=schedule.interval_seconds,
            )

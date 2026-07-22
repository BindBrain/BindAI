from __future__ import annotations


class RequestPipeline:
    def __init__(self):

        self._steps = []

    def add(
        self,
        step,
    ):

        self._steps.append(
            step,
        )

    def execute(
        self,
        agent,
        context,
        request,
    ):

        for step in self._steps:
            request = step.process(
                agent,
                context,
                request,
            )

        return request

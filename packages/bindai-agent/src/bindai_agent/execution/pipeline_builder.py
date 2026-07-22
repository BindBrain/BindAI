from __future__ import annotations

from .pipeline import ExecutionPipeline
from .step import ExecutionStep


class PipelineBuilder:
    def __init__(self):
        self._steps: list[ExecutionStep] = []

    def add(
        self,
        step: ExecutionStep,
    ) -> "PipelineBuilder":
        self._steps.append(step)
        return self

    def build(
        self,
    ) -> ExecutionPipeline:
        return ExecutionPipeline(
            self._steps,
        )
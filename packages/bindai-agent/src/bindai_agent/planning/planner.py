from abc import ABC
from abc import abstractmethod

from .plan import ExecutionPlan


class Planner(ABC):
    @abstractmethod
    def create_plan(
        self,
        agent,
        context,
    ) -> ExecutionPlan: ...

    @abstractmethod
    def revise_plan(
        self,
        plan,
        context,
    ) -> ExecutionPlan: ...

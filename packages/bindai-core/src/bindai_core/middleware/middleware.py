from abc import ABC, abstractmethod


class Middleware(ABC):
    @abstractmethod
    def before_execute(
        self,
        agent,
        context,
    ): ...

    @abstractmethod
    def after_execute(
        self,
        agent,
        context,
        result,
    ): ...

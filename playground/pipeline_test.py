from bindai_core import (
    ExecutionPipeline,
    ExecutionContext,
)


class MiddlewareOne:
    def before_execute(
        self,
        agent,
        context,
    ):
        print("Middleware One")

    def after_execute(
        self,
        agent,
        context,
        result,
    ):
        pass


class MiddlewareTwo:
    def before_execute(
        self,
        agent,
        context,
    ):
        print("Middleware Two")

    def after_execute(
        self,
        agent,
        context,
        result,
    ):
        pass


class DummyAgent:
    def execute(
        self,
        context,
    ):
        return None


pipeline = ExecutionPipeline()

pipeline.use(MiddlewareOne())
pipeline.use(MiddlewareTwo())

pipeline.execute(
    DummyAgent(),
    ExecutionContext(),
)

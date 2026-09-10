from bindai_core.context import ExecutionContext
from bindai_core.executable import Executable, ExecutionResult

from bindai_automation import AutomationDefinition


class SampleExecutable(Executable):
    def execute(self, context: ExecutionContext) -> ExecutionResult:
        return ExecutionResult(success=True, output="done")


def test_definition_has_identity_and_target():
    target = SampleExecutable()
    definition = AutomationDefinition(name="test-automation", target=target)

    assert definition.name == "test-automation"
    assert definition.target is target
    assert definition.version == 1
    assert definition.id
    assert definition.metadata == {}


def test_definition_runs_target():
    target = SampleExecutable()
    definition = AutomationDefinition(name="test-automation", target=target)

    result = definition.run()

    assert result.success is True
    assert result.output == "done"


def test_definition_uses_provided_context():
    class ContextExecutable(Executable):
        def execute(self, context: ExecutionContext) -> ExecutionResult:
            return ExecutionResult(
                success=True,
                output=context,
            )

    target = ContextExecutable()
    definition = AutomationDefinition(name="test-automation", target=target)
    context = ExecutionContext()

    result = definition.run(context)

    assert result.success is True
    assert result.output is context


def test_definition_clone_creates_new_version():
    target = SampleExecutable()
    definition = AutomationDefinition(
        name="test-automation",
        target=target,
        metadata={"environment": "test"},
    )

    clone = definition.clone()

    assert clone is not definition
    assert clone.id == definition.id
    assert clone.name == definition.name
    assert clone.version == 2
    assert clone.metadata == definition.metadata
    assert clone.metadata is not definition.metadata
    assert definition.version == 1
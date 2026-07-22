from bindai_core.context import ExecutionContext


def test_context_creation():

    context = ExecutionContext()

    assert context.execution_id is not None


def test_variables():

    context = ExecutionContext()

    context.variables.set(
        "x",
        100,
    )

    assert context.variables.get("x") == 100


def test_remove_variable():

    context = ExecutionContext()

    context.variables.set(
        "name",
        "BindAI",
    )

    context.variables.remove("name")

    assert not context.variables.contains("name")


def test_clear_variables():

    context = ExecutionContext()

    context.variables.set(
        "a",
        1,
    )

    context.variables.clear()

    assert context.variables.as_dict() == {}

import pytest
from bindai_workflow.expression import WorkflowExpression


def test_expression_evaluates_workflow_conditions():
    evaluator = WorkflowExpression()

    assert evaluator.evaluate("score >= 80", {"score": 90})
    assert evaluator.evaluate(
        "status == 'ready' and retries < 3",
        {
            "status": "ready",
            "retries": 2,
        },
    )


def test_expression_supports_workflow_literals():
    evaluator = WorkflowExpression()

    assert evaluator.evaluate("true", {})
    assert not evaluator.evaluate("false", {})
    assert evaluator.evaluate("value is null", {"value": None})
    assert evaluator.evaluate("'python' in languages", {"languages": ["python"]})


def test_expression_supports_basic_arithmetic():
    evaluator = WorkflowExpression()

    assert evaluator.evaluate("attempts + 1 == 3", {"attempts": 2})
    assert evaluator.evaluate("score * 2 >= threshold", {"score": 50, "threshold": 100})


def test_expression_supports_chained_comparisons():
    evaluator = WorkflowExpression()

    assert evaluator.evaluate(
        "0 <= score <= 100",
        {"score": 75},
    )


def test_expression_rejects_unknown_variables():
    evaluator = WorkflowExpression()

    with pytest.raises(ValueError, match="Unknown variable"):
        evaluator.evaluate("missing == 1", {})


def test_expression_rejects_function_calls():
    evaluator = WorkflowExpression()

    with pytest.raises(ValueError, match="Unsupported expression construct"):
        evaluator.evaluate("str(value) == 'hello'", {"value": "hello"})


def test_expression_rejects_attribute_access():
    evaluator = WorkflowExpression()

    with pytest.raises(ValueError, match="Unsupported expression construct"):
        evaluator.evaluate("value.real > 0", {"value": 1})


def test_expression_rejects_code_execution():
    evaluator = WorkflowExpression()

    with pytest.raises(ValueError, match="Unsupported expression construct"):
        evaluator.evaluate(
            "__import__('os').system('echo ARBITRARY CODE EXECUTED')",
            {},
        )


def test_expression_rejects_dunder_names():
    evaluator = WorkflowExpression()

    with pytest.raises(ValueError, match="Dunder names"):
        evaluator.evaluate("__import__", {})


def test_expression_rejects_comprehensions():
    evaluator = WorkflowExpression()

    with pytest.raises(ValueError, match="Unsupported expression construct"):
        evaluator.evaluate(
            "[x for x in values]",
            {"values": [1, 2, 3]},
        )


def test_expression_rejects_lambda_expressions():
    evaluator = WorkflowExpression()

    with pytest.raises(ValueError, match="Unsupported expression construct"):
        evaluator.evaluate(
            "(lambda x: x)(1)",
            {},
        )


def test_expression_rejects_invalid_syntax():
    evaluator = WorkflowExpression()

    with pytest.raises(ValueError, match="Invalid workflow expression"):
        evaluator.evaluate("score >=", {"score": 90})
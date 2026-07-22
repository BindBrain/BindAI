from __future__ import annotations


class WorkflowExpression:
    """
    Small expression evaluator.

    Expressions are evaluated
    against workflow variables.
    """

    def evaluate(
        self,
        expression: str,
        variables,
    ) -> bool:

        scope = {key: value for key, value in variables.items()}

        scope["true"] = True
        scope["false"] = False
        scope["null"] = None

        return bool(
            eval(
                expression,
                {},
                scope,
            )
        )

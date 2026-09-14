from __future__ import annotations

import ast
import operator
from typing import Any


class WorkflowExpression:
    """
    Small, restricted expression evaluator.

    Expressions are evaluated against workflow variables. Only boolean
    logic, comparisons, literals, names, and basic arithmetic are supported.
    Python function calls, attribute access, imports, comprehensions, and
    other executable constructs are intentionally rejected.
    """

    _binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    _comparison_operators = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.In: lambda left, right: left in right,
        ast.NotIn: lambda left, right: left not in right,
        ast.Is: operator.is_,
        ast.IsNot: operator.is_not,
    }

    _unary_operators = {
        ast.Not: operator.not_,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def evaluate(
        self,
        expression: str,
        variables: dict[str, Any],
    ) -> bool:
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError("Invalid workflow expression.") from exc

        scope = dict(variables)
        scope["true"] = True
        scope["false"] = False
        scope["null"] = None

        return bool(self._evaluate_node(tree.body, scope))

    def _evaluate_node(
        self,
        node: ast.AST,
        scope: dict[str, Any],
    ) -> Any:
        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.Name):
            if node.id.startswith("__"):
                raise ValueError("Dunder names are not allowed in workflow expressions.")

            if node.id not in scope:
                raise ValueError(
                    f"Unknown variable '{node.id}' in workflow expression."
                )

            return scope[node.id]

        if isinstance(node, ast.List):
            return [self._evaluate_node(element, scope) for element in node.elts]

        if isinstance(node, ast.Tuple):
            return tuple(
                self._evaluate_node(element, scope)
                for element in node.elts
            )

        if isinstance(node, ast.Set):
            return {
                self._evaluate_node(element, scope)
                for element in node.elts
            }

        if isinstance(node, ast.Dict):
            return {
                self._evaluate_node(key, scope): self._evaluate_node(value, scope)
                for key, value in zip(node.keys, node.values)
            }

        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                result = True
                for value in node.values:
                    result = self._evaluate_node(value, scope)
                    if not result:
                        return result
                return result

            if isinstance(node.op, ast.Or):
                result = False
                for value in node.values:
                    result = self._evaluate_node(value, scope)
                    if result:
                        return result
                return result

            raise ValueError("Unsupported boolean operator.")

        if isinstance(node, ast.UnaryOp):
            operator_function = self._unary_operators.get(type(node.op))
            if operator_function is None:
                raise ValueError("Unsupported unary operator.")

            return operator_function(
                self._evaluate_node(node.operand, scope)
            )

        if isinstance(node, ast.BinOp):
            operator_function = self._binary_operators.get(type(node.op))
            if operator_function is None:
                raise ValueError("Unsupported binary operator.")

            return operator_function(
                self._evaluate_node(node.left, scope),
                self._evaluate_node(node.right, scope),
            )

        if isinstance(node, ast.Compare):
            left = self._evaluate_node(node.left, scope)

            for operator_node, comparator in zip(
                node.ops,
                node.comparators,
            ):
                operator_function = self._comparison_operators.get(
                    type(operator_node)
                )

                if operator_function is None:
                    raise ValueError("Unsupported comparison operator.")

                right = self._evaluate_node(comparator, scope)

                if not operator_function(left, right):
                    return False

                left = right

            return True

        raise ValueError(
            f"Unsupported expression construct: {type(node).__name__}."
        )
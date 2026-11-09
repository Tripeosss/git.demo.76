import ast
import operator
import math
from typing import Any
from agent.tools.base import BaseTool

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_ALLOWED_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "abs": abs,
    "round": round,
    "pi": math.pi,
    "e": math.e,
}


class CalculatorTool(BaseTool):
    name = "calculator"
    description = (
        "Calculates mathematical expressions. Input should be a valid math string, "
        "e.g., '2 * (3 + 5)', 'sqrt(144) + 10'."
    )

    def _eval(self, node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return self._eval(node.body)
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                return _ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval(node.operand)
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                return _ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in _ALLOWED_FUNCTIONS:
                func = _ALLOWED_FUNCTIONS[node.func.id]
                args = [self._eval(arg) for arg in node.args]
                return func(*args)
            raise ValueError(f"Unsupported function call: {ast.dump(node)}")
        elif isinstance(node, ast.Name):
            if node.id in _ALLOWED_FUNCTIONS:
                return _ALLOWED_FUNCTIONS[node.id]
            raise ValueError(f"Unknown variable: {node.id}")
        else:
            raise TypeError(f"Unsupported expression node: {type(node).__name__}")

    def run(self, expression: str) -> str:
        try:
            expr = str(expression).strip()
            parsed = ast.parse(expr, mode="eval")
            result = self._eval(parsed)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation Error: {str(e)}"

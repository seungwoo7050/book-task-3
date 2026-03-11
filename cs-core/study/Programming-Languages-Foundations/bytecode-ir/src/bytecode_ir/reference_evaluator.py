from __future__ import annotations

from dataclasses import dataclass

from .ast import BinaryOp, BooleanLiteral, CallExpr, Expr, FunExpr, Identifier, IfExpr, IntegerLiteral, LetExpr, Param, UnaryOp
from .diagnostics import Diagnostic, RuntimeDiagnosticError


@dataclass
class Environment:
    values: dict[str, object]
    parent: "Environment | None" = None

    def lookup(self, name: str) -> object:
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        raise RuntimeDiagnosticError(Diagnostic(f"unbound name '{name}'", 0, 0))


@dataclass(frozen=True)
class ClosureValue:
    params: tuple[Param, ...]
    body: Expr
    environment: Environment


def evaluate_source(source: str) -> object:
    from .parser import parse_source

    return evaluate_expression(parse_source(source))


def evaluate_expression(expression: Expr, environment: Environment | None = None) -> object:
    env = environment or Environment({})
    if isinstance(expression, IntegerLiteral):
        return expression.value
    if isinstance(expression, BooleanLiteral):
        return expression.value
    if isinstance(expression, Identifier):
        return env.lookup(expression.name)
    if isinstance(expression, UnaryOp):
        value = evaluate_expression(expression.operand, env)
        if expression.operator == "-":
            return -_require_int(value, "operator - requires Int operand")
        if expression.operator == "not":
            return not _require_bool(value, "operator not requires Bool operand")
    if isinstance(expression, BinaryOp):
        if expression.operator == "and":
            left = _require_bool(evaluate_expression(expression.left, env), "operator and requires Bool operands")
            if not left:
                return False
            return _require_bool(evaluate_expression(expression.right, env), "operator and requires Bool operands")
        if expression.operator == "or":
            left = _require_bool(evaluate_expression(expression.left, env), "operator or requires Bool operands")
            if left:
                return True
            return _require_bool(evaluate_expression(expression.right, env), "operator or requires Bool operands")
        left = evaluate_expression(expression.left, env)
        right = evaluate_expression(expression.right, env)
        if expression.operator == "+":
            return _require_int(left, "operator + requires Int operands") + _require_int(right, "operator + requires Int operands")
        if expression.operator == "-":
            return _require_int(left, "operator - requires Int operands") - _require_int(right, "operator - requires Int operands")
        if expression.operator == "*":
            return _require_int(left, "operator * requires Int operands") * _require_int(right, "operator * requires Int operands")
        if expression.operator == "/":
            divisor = _require_int(right, "operator / requires Int operands")
            if divisor == 0:
                raise RuntimeDiagnosticError(Diagnostic("division by zero", 0, 0))
            return _require_int(left, "operator / requires Int operands") // divisor
        if expression.operator == "<":
            return _require_int(left, "operator < requires Int operands") < _require_int(right, "operator < requires Int operands")
        if expression.operator == "<=":
            return _require_int(left, "operator <= requires Int operands") <= _require_int(right, "operator <= requires Int operands")
        if expression.operator == ">":
            return _require_int(left, "operator > requires Int operands") > _require_int(right, "operator > requires Int operands")
        if expression.operator == ">=":
            return _require_int(left, "operator >= requires Int operands") >= _require_int(right, "operator >= requires Int operands")
        if expression.operator in {"==", "!="}:
            result = _compare_values(left, right, expression.operator)
            return result if expression.operator == "==" else not result
    if isinstance(expression, LetExpr):
        value = evaluate_expression(expression.value, env)
        child = Environment({expression.name: value}, parent=env)
        return evaluate_expression(expression.body, child)
    if isinstance(expression, IfExpr):
        condition = _require_bool(evaluate_expression(expression.condition, env), "if condition must be Bool")
        return evaluate_expression(expression.then_branch if condition else expression.else_branch, env)
    if isinstance(expression, FunExpr):
        return ClosureValue(expression.params, expression.body, env)
    if isinstance(expression, CallExpr):
        callee = evaluate_expression(expression.callee, env)
        if not isinstance(callee, ClosureValue):
            raise RuntimeDiagnosticError(Diagnostic("attempted to call a non-function value", 0, 0))
        if len(expression.arguments) != len(callee.params):
            raise RuntimeDiagnosticError(Diagnostic(f"expected {len(callee.params)} arguments, got {len(expression.arguments)}", 0, 0))
        values = {
            param.name: evaluate_expression(argument, env)
            for param, argument in zip(callee.params, expression.arguments, strict=True)
        }
        child = Environment(values, parent=callee.environment)
        return evaluate_expression(callee.body, child)
    raise RuntimeDiagnosticError(Diagnostic(f"unsupported expression '{expression!r}'", 0, 0))


def _require_int(value: object, message: str) -> int:
    if type(value) is int:
        return value
    raise RuntimeDiagnosticError(Diagnostic(message, 0, 0))


def _require_bool(value: object, message: str) -> bool:
    if type(value) is bool:
        return value
    raise RuntimeDiagnosticError(Diagnostic(message, 0, 0))


def _compare_values(left: object, right: object, symbol: str) -> bool:
    if isinstance(left, ClosureValue) or isinstance(right, ClosureValue):
        raise RuntimeDiagnosticError(Diagnostic(f"operator {symbol} cannot compare function values", 0, 0))
    if type(left) is not type(right):
        raise RuntimeDiagnosticError(Diagnostic(f"operator {symbol} requires operands of the same type", 0, 0))
    if type(left) not in {int, bool}:
        raise RuntimeDiagnosticError(Diagnostic(f"operator {symbol} only supports Int and Bool", 0, 0))
    return left == right

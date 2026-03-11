from __future__ import annotations

from dataclasses import dataclass

from .ast import BinaryOp, BooleanLiteral, CallExpr, Expr, FunExpr, Identifier, IfExpr, IntegerLiteral, LetExpr, UnaryOp
from .ast import Param, format_type
from .diagnostics import Diagnostic, RuntimeDiagnosticError
from .environment import Environment


@dataclass(frozen=True)
class Closure:
    params: tuple[Param, ...]
    return_annotation: object | None
    body: Expr
    environment: Environment

    def signature(self) -> str:
        params = []
        for param in self.params:
            if param.annotation is None:
                params.append(param.name)
            else:
                params.append(f"{param.name}: {format_type(param.annotation)}")
        if self.return_annotation is None:
            return f"fun ({', '.join(params)})"
        return f"fun ({', '.join(params)}) -> {format_type(self.return_annotation)}"


def evaluate_expression(expr: Expr, environment: Environment | None = None) -> object:
    env = environment or Environment()
    if isinstance(expr, IntegerLiteral):
        return expr.value
    if isinstance(expr, BooleanLiteral):
        return expr.value
    if isinstance(expr, Identifier):
        return env.lookup(expr.name)
    if isinstance(expr, UnaryOp):
        value = evaluate_expression(expr.operand, env)
        if expr.operator == "-":
            return -_require_int(value, "unary '-'")
        if expr.operator == "not":
            return not _require_bool(value, "'not'")
        raise RuntimeDiagnosticError(Diagnostic(f"unsupported unary operator '{expr.operator}'", 0, 0))
    if isinstance(expr, BinaryOp):
        if expr.operator == "and":
            left = _require_bool(evaluate_expression(expr.left, env), "'and'")
            if not left:
                return False
            return _require_bool(evaluate_expression(expr.right, env), "'and'")
        if expr.operator == "or":
            left = _require_bool(evaluate_expression(expr.left, env), "'or'")
            if left:
                return True
            return _require_bool(evaluate_expression(expr.right, env), "'or'")

        left = evaluate_expression(expr.left, env)
        right = evaluate_expression(expr.right, env)
        if expr.operator in {"+", "-", "*", "/"}:
            left_int = _require_int(left, expr.operator)
            right_int = _require_int(right, expr.operator)
            if expr.operator == "+":
                return left_int + right_int
            if expr.operator == "-":
                return left_int - right_int
            if expr.operator == "*":
                return left_int * right_int
            if right_int == 0:
                raise RuntimeDiagnosticError(Diagnostic("division by zero", 0, 0))
            return left_int // right_int
        if expr.operator in {"<", "<=", ">", ">="}:
            left_int = _require_int(left, expr.operator)
            right_int = _require_int(right, expr.operator)
            if expr.operator == "<":
                return left_int < right_int
            if expr.operator == "<=":
                return left_int <= right_int
            if expr.operator == ">":
                return left_int > right_int
            return left_int >= right_int
        if expr.operator in {"==", "!="}:
            result = _compare_primitives(left, right, expr.operator)
            return result if expr.operator == "==" else not result
        raise RuntimeDiagnosticError(Diagnostic(f"unsupported binary operator '{expr.operator}'", 0, 0))
    if isinstance(expr, LetExpr):
        value = evaluate_expression(expr.value, env)
        child = Environment(parent=env)
        child.define(expr.name, value)
        return evaluate_expression(expr.body, child)
    if isinstance(expr, IfExpr):
        condition = _require_bool(evaluate_expression(expr.condition, env), "'if'")
        branch = expr.then_branch if condition else expr.else_branch
        return evaluate_expression(branch, env)
    if isinstance(expr, FunExpr):
        return Closure(expr.params, expr.return_annotation, expr.body, env)
    if isinstance(expr, CallExpr):
        callee = evaluate_expression(expr.callee, env)
        if not isinstance(callee, Closure):
            raise RuntimeDiagnosticError(Diagnostic("attempted to call a non-function value", 0, 0))
        if len(expr.arguments) != len(callee.params):
            raise RuntimeDiagnosticError(
                Diagnostic(
                    f"expected {len(callee.params)} arguments, got {len(expr.arguments)}",
                    0,
                    0,
                )
            )
        call_env = Environment(parent=callee.environment)
        for param, argument in zip(callee.params, expr.arguments, strict=True):
            call_env.define(param.name, evaluate_expression(argument, env))
        return evaluate_expression(callee.body, call_env)
    raise RuntimeDiagnosticError(Diagnostic(f"unsupported expression '{expr!r}'", 0, 0))


def evaluate_source(source: str) -> object:
    from .parser import parse_source

    return evaluate_expression(parse_source(source))


def format_value(value: object) -> str:
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        return str(value)
    if isinstance(value, Closure):
        return f"<closure {value.signature()}>"
    return repr(value)


def _require_int(value: object, operator: str) -> int:
    if type(value) is int:
        return value
    raise RuntimeDiagnosticError(Diagnostic(f"operator {operator} requires Int operands", 0, 0))


def _require_bool(value: object, operator: str) -> bool:
    if type(value) is bool:
        return value
    raise RuntimeDiagnosticError(Diagnostic(f"operator {operator} requires Bool operands", 0, 0))


def _compare_primitives(left: object, right: object, operator: str) -> bool:
    if isinstance(left, Closure) or isinstance(right, Closure):
        raise RuntimeDiagnosticError(Diagnostic(f"operator {operator} cannot compare function values", 0, 0))
    if type(left) is not type(right):
        raise RuntimeDiagnosticError(Diagnostic(f"operator {operator} requires operands of the same type", 0, 0))
    if type(left) not in {int, bool}:
        raise RuntimeDiagnosticError(Diagnostic(f"operator {operator} only supports Int and Bool", 0, 0))
    return left == right

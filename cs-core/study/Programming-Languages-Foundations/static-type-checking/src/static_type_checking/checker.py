from __future__ import annotations

from dataclasses import dataclass, field

from .ast import (
    BinaryOp,
    BoolType,
    BooleanLiteral,
    CallExpr,
    Expr,
    FunctionType,
    FunExpr,
    Identifier,
    IfExpr,
    IntType,
    IntegerLiteral,
    LetExpr,
    TypeExpr,
    UnaryOp,
    format_type,
)
from .diagnostics import Diagnostic, TypeDiagnosticError


@dataclass
class TypeEnvironment:
    bindings: dict[str, TypeExpr] = field(default_factory=dict)
    parent: "TypeEnvironment | None" = None

    def define(self, name: str, type_expr: TypeExpr) -> None:
        self.bindings[name] = type_expr

    def lookup(self, name: str, line: int, column: int) -> TypeExpr:
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.lookup(name, line, column)
        raise TypeDiagnosticError(Diagnostic(f"unbound name '{name}'", line, column))


def check_expression(expr: Expr, environment: TypeEnvironment | None = None) -> TypeExpr:
    env = environment or TypeEnvironment()
    if isinstance(expr, IntegerLiteral):
        return IntType()
    if isinstance(expr, BooleanLiteral):
        return BoolType()
    if isinstance(expr, Identifier):
        return env.lookup(expr.name, expr.line, expr.column)
    if isinstance(expr, UnaryOp):
        operand_type = check_expression(expr.operand, env)
        if expr.operator == "-":
            _expect_exact_type(operand_type, IntType(), expr.line, expr.column, "operator - requires Int operand")
            return IntType()
        if expr.operator == "not":
            _expect_exact_type(operand_type, BoolType(), expr.line, expr.column, "operator not requires Bool operand")
            return BoolType()
        raise TypeDiagnosticError(Diagnostic(f"unsupported unary operator '{expr.operator}'", expr.line, expr.column))
    if isinstance(expr, BinaryOp):
        left_type = check_expression(expr.left, env)
        right_type = check_expression(expr.right, env)
        if expr.operator in {"+", "-", "*", "/"}:
            _expect_exact_type(left_type, IntType(), expr.line, expr.column, f"operator {expr.operator} requires Int operands")
            _expect_exact_type(right_type, IntType(), expr.line, expr.column, f"operator {expr.operator} requires Int operands")
            return IntType()
        if expr.operator in {"<", "<=", ">", ">="}:
            _expect_exact_type(left_type, IntType(), expr.line, expr.column, f"operator {expr.operator} requires Int operands")
            _expect_exact_type(right_type, IntType(), expr.line, expr.column, f"operator {expr.operator} requires Int operands")
            return BoolType()
        if expr.operator in {"and", "or"}:
            _expect_exact_type(left_type, BoolType(), expr.line, expr.column, f"operator {expr.operator} requires Bool operands")
            _expect_exact_type(right_type, BoolType(), expr.line, expr.column, f"operator {expr.operator} requires Bool operands")
            return BoolType()
        if expr.operator in {"==", "!="}:
            if isinstance(left_type, FunctionType) or isinstance(right_type, FunctionType):
                raise TypeDiagnosticError(Diagnostic(f"operator {expr.operator} cannot compare function values", expr.line, expr.column))
            if left_type != right_type:
                raise TypeDiagnosticError(
                    Diagnostic(
                        f"operator {expr.operator} requires operands of the same type, got {format_type(left_type)} and {format_type(right_type)}",
                        expr.line,
                        expr.column,
                    )
                )
            return BoolType()
        raise TypeDiagnosticError(Diagnostic(f"unsupported binary operator '{expr.operator}'", expr.line, expr.column))
    if isinstance(expr, LetExpr):
        value_type = check_expression(expr.value, env)
        binding_type = value_type
        if expr.annotation is not None:
            if expr.annotation != value_type:
                raise TypeDiagnosticError(
                    Diagnostic(
                        f"let binding '{expr.name}' expected {format_type(expr.annotation)}, got {format_type(value_type)}",
                        expr.line,
                        expr.column,
                    )
                )
            binding_type = expr.annotation
        child = TypeEnvironment(parent=env)
        child.define(expr.name, binding_type)
        return check_expression(expr.body, child)
    if isinstance(expr, IfExpr):
        condition_type = check_expression(expr.condition, env)
        _expect_exact_type(condition_type, BoolType(), expr.condition.line, expr.condition.column, f"if condition must be Bool, got {format_type(condition_type)}")
        then_type = check_expression(expr.then_branch, env)
        else_type = check_expression(expr.else_branch, env)
        if then_type != else_type:
            raise TypeDiagnosticError(
                Diagnostic(
                    f"if branches must have same type, got {format_type(then_type)} and {format_type(else_type)}",
                    expr.line,
                    expr.column,
                )
            )
        return then_type
    if isinstance(expr, FunExpr):
        parameter_types = []
        function_env = TypeEnvironment(parent=env)
        for param in expr.params:
            if param.annotation is None:
                raise TypeDiagnosticError(
                    Diagnostic(f"parameter '{param.name}' requires a type annotation", param.line, param.column)
                )
            parameter_types.append(param.annotation)
            function_env.define(param.name, param.annotation)
        if expr.return_annotation is None:
            raise TypeDiagnosticError(Diagnostic("function return type annotation is required", expr.line, expr.column))
        body_type = check_expression(expr.body, function_env)
        if body_type != expr.return_annotation:
            raise TypeDiagnosticError(
                Diagnostic(
                    f"function return expected {format_type(expr.return_annotation)}, got {format_type(body_type)}",
                    expr.body.line,
                    expr.body.column,
                )
            )
        return FunctionType(tuple(parameter_types), expr.return_annotation)
    if isinstance(expr, CallExpr):
        callee_type = check_expression(expr.callee, env)
        if not isinstance(callee_type, FunctionType):
            raise TypeDiagnosticError(Diagnostic("attempted to call a non-function type", expr.line, expr.column))
        if len(expr.arguments) != len(callee_type.params):
            raise TypeDiagnosticError(
                Diagnostic(
                    f"expected {len(callee_type.params)} arguments, got {len(expr.arguments)}",
                    expr.line,
                    expr.column,
                )
            )
        for index, (argument, expected_type) in enumerate(zip(expr.arguments, callee_type.params, strict=True), start=1):
            actual_type = check_expression(argument, env)
            if actual_type != expected_type:
                raise TypeDiagnosticError(
                    Diagnostic(
                        f"argument {index} expected {format_type(expected_type)}, got {format_type(actual_type)}",
                        argument.line,
                        argument.column,
                    )
                )
        return callee_type.return_type
    raise TypeDiagnosticError(Diagnostic(f"unsupported expression '{expr!r}'", expr.line, expr.column))


def check_source(source: str) -> TypeExpr:
    from .parser import parse_source

    return check_expression(parse_source(source))


def _expect_exact_type(actual: TypeExpr, expected: TypeExpr, line: int, column: int, message: str) -> None:
    if actual != expected:
        raise TypeDiagnosticError(Diagnostic(message, line, column))

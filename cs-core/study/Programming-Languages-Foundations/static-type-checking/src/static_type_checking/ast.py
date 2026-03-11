from __future__ import annotations

from dataclasses import dataclass


class TypeExpr:
    pass


@dataclass(frozen=True)
class IntType(TypeExpr):
    pass


@dataclass(frozen=True)
class BoolType(TypeExpr):
    pass


@dataclass(frozen=True)
class FunctionType(TypeExpr):
    params: tuple[TypeExpr, ...]
    return_type: TypeExpr


@dataclass(frozen=True)
class Param:
    name: str
    annotation: TypeExpr | None
    line: int
    column: int


class Expr:
    line: int
    column: int


@dataclass(frozen=True)
class IntegerLiteral(Expr):
    value: int
    line: int
    column: int


@dataclass(frozen=True)
class BooleanLiteral(Expr):
    value: bool
    line: int
    column: int


@dataclass(frozen=True)
class Identifier(Expr):
    name: str
    line: int
    column: int


@dataclass(frozen=True)
class UnaryOp(Expr):
    operator: str
    operand: Expr
    line: int
    column: int


@dataclass(frozen=True)
class BinaryOp(Expr):
    operator: str
    left: Expr
    right: Expr
    line: int
    column: int


@dataclass(frozen=True)
class LetExpr(Expr):
    name: str
    annotation: TypeExpr | None
    value: Expr
    body: Expr
    line: int
    column: int


@dataclass(frozen=True)
class IfExpr(Expr):
    condition: Expr
    then_branch: Expr
    else_branch: Expr
    line: int
    column: int


@dataclass(frozen=True)
class FunExpr(Expr):
    params: tuple[Param, ...]
    return_annotation: TypeExpr | None
    body: Expr
    line: int
    column: int


@dataclass(frozen=True)
class CallExpr(Expr):
    callee: Expr
    arguments: tuple[Expr, ...]
    line: int
    column: int


def format_type(type_expr: TypeExpr) -> str:
    if isinstance(type_expr, IntType):
        return "Int"
    if isinstance(type_expr, BoolType):
        return "Bool"
    if isinstance(type_expr, FunctionType):
        params = ", ".join(format_type(param) for param in type_expr.params)
        if len(type_expr.params) != 1 or (
            len(type_expr.params) == 1 and isinstance(type_expr.params[0], FunctionType)
        ):
            params = f"({params})"
        return f"{params} -> {format_type(type_expr.return_type)}"
    raise TypeError(f"unsupported type node: {type_expr!r}")

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
    annotation: TypeExpr | None = None


class Expr:
    pass


@dataclass(frozen=True)
class IntegerLiteral(Expr):
    value: int


@dataclass(frozen=True)
class BooleanLiteral(Expr):
    value: bool


@dataclass(frozen=True)
class Identifier(Expr):
    name: str


@dataclass(frozen=True)
class UnaryOp(Expr):
    operator: str
    operand: Expr


@dataclass(frozen=True)
class BinaryOp(Expr):
    operator: str
    left: Expr
    right: Expr


@dataclass(frozen=True)
class LetExpr(Expr):
    name: str
    annotation: TypeExpr | None
    value: Expr
    body: Expr


@dataclass(frozen=True)
class IfExpr(Expr):
    condition: Expr
    then_branch: Expr
    else_branch: Expr


@dataclass(frozen=True)
class FunExpr(Expr):
    params: tuple[Param, ...]
    return_annotation: TypeExpr | None
    body: Expr


@dataclass(frozen=True)
class CallExpr(Expr):
    callee: Expr
    arguments: tuple[Expr, ...]


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


def _indent(level: int) -> str:
    return "  " * level


def _format_param(param: Param) -> str:
    if param.annotation is None:
        return param.name
    return f"{param.name}: {format_type(param.annotation)}"


def format_expr(expr: Expr, level: int = 0) -> str:
    pad = _indent(level)
    if isinstance(expr, IntegerLiteral):
        return f"{pad}Integer({expr.value})"
    if isinstance(expr, BooleanLiteral):
        value = "true" if expr.value else "false"
        return f"{pad}Boolean({value})"
    if isinstance(expr, Identifier):
        return f"{pad}Identifier({expr.name})"
    if isinstance(expr, UnaryOp):
        return "\n".join(
            [
                f"{pad}Unary({expr.operator})",
                format_expr(expr.operand, level + 1),
            ]
        )
    if isinstance(expr, BinaryOp):
        return "\n".join(
            [
                f"{pad}Binary({expr.operator})",
                format_expr(expr.left, level + 1),
                format_expr(expr.right, level + 1),
            ]
        )
    if isinstance(expr, LetExpr):
        label = expr.name
        if expr.annotation is not None:
            label = f"{label}: {format_type(expr.annotation)}"
        return "\n".join(
            [
                f"{pad}Let({label})",
                f"{pad}value:",
                format_expr(expr.value, level + 1),
                f"{pad}body:",
                format_expr(expr.body, level + 1),
            ]
        )
    if isinstance(expr, IfExpr):
        return "\n".join(
            [
                f"{pad}If",
                f"{pad}condition:",
                format_expr(expr.condition, level + 1),
                f"{pad}then:",
                format_expr(expr.then_branch, level + 1),
                f"{pad}else:",
                format_expr(expr.else_branch, level + 1),
            ]
        )
    if isinstance(expr, FunExpr):
        params = ", ".join(_format_param(param) for param in expr.params)
        if expr.return_annotation is None:
            signature = f"({params})"
        else:
            signature = f"({params}) -> {format_type(expr.return_annotation)}"
        return "\n".join(
            [
                f"{pad}Fun{signature}",
                format_expr(expr.body, level + 1),
            ]
        )
    if isinstance(expr, CallExpr):
        lines = [f"{pad}Call", f"{pad}callee:", format_expr(expr.callee, level + 1)]
        lines.append(f"{pad}args:")
        if expr.arguments:
            lines.extend(format_expr(argument, level + 1) for argument in expr.arguments)
        else:
            lines.append(f"{_indent(level + 1)}<empty>")
        return "\n".join(lines)
    raise TypeError(f"unsupported expr node: {expr!r}")

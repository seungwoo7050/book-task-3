from __future__ import annotations

from dataclasses import dataclass, field

from .ast import BinaryOp, BooleanLiteral, CallExpr, Expr, FunExpr, Identifier, IfExpr, IntegerLiteral, LetExpr, UnaryOp
from .diagnostics import CompileDiagnosticError, Diagnostic


@dataclass(frozen=True)
class SourceRef:
    kind: str
    index: int
    name: str


@dataclass(frozen=True)
class Instruction:
    op: str
    arg: object | None = None


@dataclass(frozen=True)
class FunctionProto:
    name: str
    arity: int
    instructions: tuple[Instruction, ...]
    local_count: int
    capture_names: tuple[str, ...]
    capture_sources: tuple[SourceRef, ...]


@dataclass
class CompileContext:
    name: str
    parent: "CompileContext | None" = None
    instructions: list[Instruction] = field(default_factory=list)
    local_bindings: dict[str, int] = field(default_factory=dict)
    capture_bindings: dict[str, int] = field(default_factory=dict)
    capture_names: list[str] = field(default_factory=list)
    capture_sources: list[SourceRef] = field(default_factory=list)
    local_count: int = 0

    def reserve_local(self) -> int:
        index = self.local_count
        self.local_count += 1
        return index

    def bind_name(self, name: str, index: int) -> None:
        self.local_bindings[name] = index

    def resolve(self, name: str) -> SourceRef | None:
        if name in self.local_bindings:
            return SourceRef("local", self.local_bindings[name], name)
        if name in self.capture_bindings:
            return SourceRef("capture", self.capture_bindings[name], name)
        if self.parent is None:
            return None
        outer = self.parent.resolve(name)
        if outer is None:
            return None
        capture_index = len(self.capture_sources)
        self.capture_bindings[name] = capture_index
        self.capture_names.append(name)
        self.capture_sources.append(outer)
        return SourceRef("capture", capture_index, name)

    def emit(self, op: str, arg: object | None = None) -> int:
        self.instructions.append(Instruction(op, arg))
        return len(self.instructions) - 1

    def patch(self, index: int, arg: int) -> None:
        instruction = self.instructions[index]
        self.instructions[index] = Instruction(instruction.op, arg)


ARITHMETIC_OPS = {
    "+": "ADD",
    "-": "SUB",
    "*": "MUL",
    "/": "DIV",
    "<": "LT",
    "<=": "LTE",
    ">": "GT",
    ">=": "GTE",
    "==": "EQ",
    "!=": "NEQ",
}


def compile_source(source: str) -> FunctionProto:
    from .parser import parse_source

    return compile_expression(parse_source(source))


def compile_expression(expression: Expr) -> FunctionProto:
    context = CompileContext("<module>")
    _compile_expr(expression, context)
    context.emit("RETURN")
    return FunctionProto(
        name=context.name,
        arity=0,
        instructions=tuple(context.instructions),
        local_count=context.local_count,
        capture_names=tuple(context.capture_names),
        capture_sources=tuple(context.capture_sources),
    )


def _compile_expr(expression: Expr, context: CompileContext) -> None:
    if isinstance(expression, IntegerLiteral):
        context.emit("PUSH_CONST", expression.value)
        return
    if isinstance(expression, BooleanLiteral):
        context.emit("PUSH_CONST", expression.value)
        return
    if isinstance(expression, Identifier):
        source = context.resolve(expression.name)
        if source is None:
            context.emit("LOAD_GLOBAL", expression.name)
            return
        context.emit("LOAD_LOCAL" if source.kind == "local" else "LOAD_CAPTURE", source.index)
        return
    if isinstance(expression, UnaryOp):
        _compile_expr(expression.operand, context)
        if expression.operator == "-":
            context.emit("NEG")
            return
        if expression.operator == "not":
            context.emit("NOT")
            return
        raise CompileDiagnosticError(Diagnostic(f"unsupported unary operator '{expression.operator}'", expression.line, expression.column))
    if isinstance(expression, BinaryOp):
        if expression.operator == "and":
            _compile_expr(expression.left, context)
            jump_false = context.emit("JUMP_IF_FALSE", None)
            _compile_expr(expression.right, context)
            jump_end = context.emit("JUMP", None)
            false_target = context.emit("PUSH_CONST", False)
            context.patch(jump_false, false_target)
            context.patch(jump_end, len(context.instructions))
            return
        if expression.operator == "or":
            _compile_expr(expression.left, context)
            jump_true = context.emit("JUMP_IF_TRUE", None)
            _compile_expr(expression.right, context)
            jump_end = context.emit("JUMP", None)
            true_target = context.emit("PUSH_CONST", True)
            context.patch(jump_true, true_target)
            context.patch(jump_end, len(context.instructions))
            return
        _compile_expr(expression.left, context)
        _compile_expr(expression.right, context)
        op = ARITHMETIC_OPS.get(expression.operator)
        if op is None:
            raise CompileDiagnosticError(Diagnostic(f"unsupported binary operator '{expression.operator}'", expression.line, expression.column))
        context.emit(op)
        return
    if isinstance(expression, LetExpr):
        _compile_expr(expression.value, context)
        slot = context.reserve_local()
        previous = context.local_bindings.get(expression.name)
        context.bind_name(expression.name, slot)
        context.emit("STORE_LOCAL", slot)
        _compile_expr(expression.body, context)
        if previous is None:
            del context.local_bindings[expression.name]
        else:
            context.local_bindings[expression.name] = previous
        return
    if isinstance(expression, IfExpr):
        _compile_expr(expression.condition, context)
        jump_false = context.emit("JUMP_IF_FALSE", None)
        _compile_expr(expression.then_branch, context)
        jump_end = context.emit("JUMP", None)
        else_target = len(context.instructions)
        context.patch(jump_false, else_target)
        _compile_expr(expression.else_branch, context)
        context.patch(jump_end, len(context.instructions))
        return
    if isinstance(expression, FunExpr):
        proto = _compile_function(expression, context)
        context.emit("MAKE_CLOSURE", proto)
        return
    if isinstance(expression, CallExpr):
        _compile_expr(expression.callee, context)
        for argument in expression.arguments:
            _compile_expr(argument, context)
        context.emit("CALL", len(expression.arguments))
        return
    raise CompileDiagnosticError(Diagnostic(f"unsupported expression '{expression!r}'", expression.line, expression.column))


def _compile_function(expression: FunExpr, parent: CompileContext) -> FunctionProto:
    context = CompileContext("<lambda>", parent=parent)
    for param in expression.params:
        slot = context.reserve_local()
        context.bind_name(param.name, slot)
    _compile_expr(expression.body, context)
    context.emit("RETURN")
    return FunctionProto(
        name=context.name,
        arity=len(expression.params),
        instructions=tuple(context.instructions),
        local_count=context.local_count,
        capture_names=tuple(context.capture_names),
        capture_sources=tuple(context.capture_sources),
    )

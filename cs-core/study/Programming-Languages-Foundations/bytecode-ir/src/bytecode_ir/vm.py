from __future__ import annotations

from dataclasses import dataclass

from .compiler import FunctionProto, Instruction, SourceRef, compile_source
from .diagnostics import Diagnostic, RuntimeDiagnosticError


UNINITIALIZED = object()


@dataclass(frozen=True)
class Closure:
    proto: FunctionProto
    captures: tuple[object, ...]


def run_source(source: str) -> object:
    return run_proto(compile_source(source))


def run_proto(proto: FunctionProto) -> object:
    return _run_closure(Closure(proto, ()), [], {})


def disassemble_source(source: str) -> str:
    return disassemble_proto(compile_source(source))


def disassemble_proto(proto: FunctionProto) -> str:
    lines: list[str] = []
    seen: set[int] = set()

    def walk(current: FunctionProto) -> None:
        marker = id(current)
        if marker in seen:
            return
        seen.add(marker)
        captures = ", ".join(current.capture_names) if current.capture_names else "-"
        lines.append(f"fn {current.name} arity={current.arity} locals={current.local_count} captures=[{captures}]")
        for index, instruction in enumerate(current.instructions):
            lines.append(f"{index:04d} {instruction.op}{_format_arg(instruction)}")
        nested = [instruction.arg for instruction in current.instructions if instruction.op == "MAKE_CLOSURE"]
        for child in nested:
            lines.append("")
            walk(child)

    walk(proto)
    return "\n".join(lines)


def _format_arg(instruction: Instruction) -> str:
    if instruction.arg is None:
        return ""
    if instruction.op == "MAKE_CLOSURE":
        proto = instruction.arg
        captures = ", ".join(proto.capture_names) if proto.capture_names else "-"
        return f" {proto.name} captures=[{captures}]"
    return f" {instruction.arg}"


def _run_closure(closure: Closure, arguments: list[object], globals_: dict[str, object]) -> object:
    if len(arguments) != closure.proto.arity:
        raise RuntimeDiagnosticError(
            Diagnostic(f"expected {closure.proto.arity} arguments, got {len(arguments)}", 0, 0)
        )
    locals_: list[object] = [UNINITIALIZED] * closure.proto.local_count
    for index, value in enumerate(arguments):
        locals_[index] = value
    stack: list[object] = []
    ip = 0
    instructions = closure.proto.instructions
    while ip < len(instructions):
        instruction = instructions[ip]
        ip += 1
        op = instruction.op
        if op == "PUSH_CONST":
            stack.append(instruction.arg)
        elif op == "LOAD_LOCAL":
            stack.append(_load_local(locals_, instruction.arg))
        elif op == "LOAD_GLOBAL":
            stack.append(_load_global(globals_, instruction.arg))
        elif op == "STORE_LOCAL":
            locals_[instruction.arg] = stack.pop()
        elif op == "LOAD_CAPTURE":
            stack.append(closure.captures[instruction.arg])
        elif op == "MAKE_CLOSURE":
            proto = instruction.arg
            captures = tuple(_resolve_source_ref(source, locals_, closure) for source in proto.capture_sources)
            stack.append(Closure(proto, captures))
        elif op == "NEG":
            stack.append(-_require_int(stack.pop(), "operator - requires Int operand"))
        elif op == "NOT":
            stack.append(not _require_bool(stack.pop(), "operator not requires Bool operand"))
        elif op in {"ADD", "SUB", "MUL", "DIV"}:
            right = _require_int(stack.pop(), f"operator {_symbol(op)} requires Int operands")
            left = _require_int(stack.pop(), f"operator {_symbol(op)} requires Int operands")
            if op == "ADD":
                stack.append(left + right)
            elif op == "SUB":
                stack.append(left - right)
            elif op == "MUL":
                stack.append(left * right)
            else:
                if right == 0:
                    raise RuntimeDiagnosticError(Diagnostic("division by zero", 0, 0))
                stack.append(left // right)
        elif op in {"LT", "LTE", "GT", "GTE"}:
            right = _require_int(stack.pop(), f"operator {_symbol(op)} requires Int operands")
            left = _require_int(stack.pop(), f"operator {_symbol(op)} requires Int operands")
            if op == "LT":
                stack.append(left < right)
            elif op == "LTE":
                stack.append(left <= right)
            elif op == "GT":
                stack.append(left > right)
            else:
                stack.append(left >= right)
        elif op in {"EQ", "NEQ"}:
            right = stack.pop()
            left = stack.pop()
            result = _compare_values(left, right, _symbol(op))
            stack.append(result if op == "EQ" else not result)
        elif op == "JUMP":
            ip = instruction.arg
        elif op == "JUMP_IF_FALSE":
            condition = _require_bool(stack.pop(), "if/jump condition must be Bool")
            if not condition:
                ip = instruction.arg
        elif op == "JUMP_IF_TRUE":
            condition = _require_bool(stack.pop(), "if/jump condition must be Bool")
            if condition:
                ip = instruction.arg
        elif op == "CALL":
            args = [stack.pop() for _ in range(instruction.arg)][::-1]
            callee = stack.pop()
            if not isinstance(callee, Closure):
                raise RuntimeDiagnosticError(Diagnostic("attempted to call a non-function value", 0, 0))
            stack.append(_run_closure(callee, args, globals_))
        elif op == "RETURN":
            if not stack:
                raise RuntimeDiagnosticError(Diagnostic("return without value", 0, 0))
            return stack.pop()
        else:
            raise RuntimeDiagnosticError(Diagnostic(f"unsupported instruction '{op}'", 0, 0))
    raise RuntimeDiagnosticError(Diagnostic("program terminated without return", 0, 0))


def _resolve_source_ref(source: SourceRef, locals_: list[object], closure: Closure) -> object:
    if source.kind == "local":
        return _load_local(locals_, source.index)
    return closure.captures[source.index]


def _load_local(locals_: list[object], index: int) -> object:
    value = locals_[index]
    if value is UNINITIALIZED:
        raise RuntimeDiagnosticError(Diagnostic(f"local slot {index} was read before initialization", 0, 0))
    return value


def _load_global(globals_: dict[str, object], name: str) -> object:
    if name not in globals_:
        raise RuntimeDiagnosticError(Diagnostic(f"unbound name '{name}'", 0, 0))
    return globals_[name]


def _require_int(value: object, message: str) -> int:
    if type(value) is int:
        return value
    raise RuntimeDiagnosticError(Diagnostic(message, 0, 0))


def _require_bool(value: object, message: str) -> bool:
    if type(value) is bool:
        return value
    raise RuntimeDiagnosticError(Diagnostic(message, 0, 0))


def _compare_values(left: object, right: object, symbol: str) -> bool:
    if isinstance(left, Closure) or isinstance(right, Closure):
        raise RuntimeDiagnosticError(Diagnostic(f"operator {symbol} cannot compare function values", 0, 0))
    if type(left) is not type(right):
        raise RuntimeDiagnosticError(Diagnostic(f"operator {symbol} requires operands of the same type", 0, 0))
    if type(left) not in {int, bool}:
        raise RuntimeDiagnosticError(Diagnostic(f"operator {symbol} only supports Int and Bool", 0, 0))
    return left == right


def _symbol(op: str) -> str:
    symbols = {
        "ADD": "+",
        "SUB": "-",
        "MUL": "*",
        "DIV": "/",
        "LT": "<",
        "LTE": "<=",
        "GT": ">",
        "GTE": ">=",
        "EQ": "==",
        "NEQ": "!=",
    }
    return symbols[op]

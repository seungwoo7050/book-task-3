import textwrap

import pytest

from bytecode_ir import RuntimeDiagnosticError, disassemble_source, run_source
from bytecode_ir.reference_evaluator import evaluate_source


def test_disassembly_golden_for_simple_program():
    source = "let choose = fun (flag: Bool) -> Int => if flag then 7 else 9 in choose(false)"
    assert (
        disassemble_source(source)
        == textwrap.dedent(
            """
            fn <module> arity=0 locals=1 captures=[-]
            0000 MAKE_CLOSURE <lambda> captures=[-]
            0001 STORE_LOCAL 0
            0002 LOAD_LOCAL 0
            0003 PUSH_CONST False
            0004 CALL 1
            0005 RETURN

            fn <lambda> arity=1 locals=1 captures=[-]
            0000 LOAD_LOCAL 0
            0001 JUMP_IF_FALSE 4
            0002 PUSH_CONST 7
            0003 JUMP 5
            0004 PUSH_CONST 9
            0005 RETURN
            """
        ).strip()
    )


@pytest.mark.parametrize(
    "source",
    [
        "1 + 2 * 3",
        "if true then 1 else 2",
        "let value = 10 in value + 5",
        "let make_adder = fun (x: Int) -> Int => fun (y: Int) -> Int => x + y in let add_two = make_adder(2) in add_two(40)",
        "let apply_twice = fun (f: Int -> Int, x: Int) -> Int => f(f(x)) in let inc = fun (n: Int) -> Int => n + 1 in apply_twice(inc, 10)",
        "if true or missing_name then 1 else 0",
    ],
)
def test_vm_matches_reference_evaluator(source: str):
    assert run_source(source) == evaluate_source(source)


def test_runtime_reports_non_callable():
    with pytest.raises(RuntimeDiagnosticError, match="attempted to call a non-function value"):
        run_source("1(2)")


def test_runtime_reports_unbound_name_when_executed():
    with pytest.raises(RuntimeDiagnosticError, match=r"unbound name 'missing_name'"):
        run_source("missing_name")

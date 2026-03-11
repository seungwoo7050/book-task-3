import textwrap

import pytest

from parser_interpreter import (
    RuntimeDiagnosticError,
    SyntaxDiagnosticError,
    evaluate_source,
    format_expr,
    parse_source,
    tokenize_source,
)


def test_lexer_tokenizes_keywords_and_type_arrows():
    source = "let inc = fun (n: Int) -> Int => n + 1 in inc(2)"
    tokens = tokenize_source(source)
    assert [token.kind for token in tokens[:10]] == [
        "LET",
        "IDENTIFIER",
        "EQUAL",
        "FUN",
        "LPAREN",
        "IDENTIFIER",
        "COLON",
        "TYPE_INT",
        "RPAREN",
        "TYPE_ARROW",
    ]
    assert tokens[0].line == 1
    assert tokens[0].column == 1


def test_parser_golden_for_let_if_call_and_annotations():
    source = textwrap.dedent(
        """
        let apply: (Int -> Int) -> Int = fun (f: Int -> Int) -> Int =>
          if true then
            f(10)
          else
            0
        in
        apply(fun (n: Int) -> Int => n + 1)
        """
    ).strip()
    expression = parse_source(source)
    assert (
        format_expr(expression)
        == textwrap.dedent(
            """
            Let(apply: (Int -> Int) -> Int)
            value:
              Fun(f: Int -> Int) -> Int
                If
                condition:
                  Boolean(true)
                then:
                  Call
                  callee:
                    Identifier(f)
                  args:
                    Integer(10)
                else:
                  Integer(0)
            body:
              Call
              callee:
                Identifier(apply)
              args:
                Fun(n: Int) -> Int
                  Binary(+)
                    Identifier(n)
                    Integer(1)
            """
        ).strip()
    )


def test_operator_precedence_and_left_associativity():
    expression = parse_source("1 + 2 * 3 - 4")
    assert (
        format_expr(expression)
        == textwrap.dedent(
            """
            Binary(-)
              Binary(+)
                Integer(1)
                Binary(*)
                  Integer(2)
                  Integer(3)
              Integer(4)
            """
        ).strip()
    )


def test_closure_uses_lexical_scope():
    source = """
    let make_adder = fun (x: Int) -> Int => fun (y: Int) -> Int => x + y in
    let add_five = make_adder(5) in
    add_five(7)
    """
    assert evaluate_source(source) == 12


def test_short_circuit_boolean_operators():
    assert evaluate_source("true or missing_name") is True
    assert evaluate_source("false and missing_name") is False


def test_annotations_are_ignored_by_runtime():
    source = """
    let inc = fun (n: Int) -> Int => n + 1 in
    let apply: (Int -> Int) -> Int = fun (f: Int -> Int) -> Int => f(10) in
    apply(inc)
    """
    assert evaluate_source(source) == 11


def test_non_bool_condition_errors():
    with pytest.raises(RuntimeDiagnosticError, match="operator 'if' requires Bool operands"):
        evaluate_source("if 1 then 2 else 3")


def test_call_arity_errors():
    source = "let add = fun (x: Int, y: Int) -> Int => x + y in add(1)"
    with pytest.raises(RuntimeDiagnosticError, match="expected 2 arguments, got 1"):
        evaluate_source(source)


def test_non_callable_errors():
    with pytest.raises(RuntimeDiagnosticError, match="attempted to call a non-function value"):
        evaluate_source("1(2)")


def test_unbound_name_errors():
    with pytest.raises(RuntimeDiagnosticError, match="unbound name 'missing_name'"):
        evaluate_source("missing_name")


def test_syntax_errors_include_line_and_column():
    with pytest.raises(SyntaxDiagnosticError, match="1:10: expected 'in' after let binding"):
        parse_source("let x = 1")

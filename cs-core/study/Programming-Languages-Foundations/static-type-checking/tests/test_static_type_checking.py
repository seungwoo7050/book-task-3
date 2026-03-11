import pytest

from static_type_checking import SyntaxDiagnosticError, TypeDiagnosticError, check_source, format_type, tokenize_source


def test_lexer_keeps_type_tokens():
    tokens = tokenize_source("fun (x: Int) -> Bool => x == 1")
    assert [token.kind for token in tokens[:8]] == [
        "FUN",
        "LPAREN",
        "IDENTIFIER",
        "COLON",
        "TYPE_INT",
        "RPAREN",
        "TYPE_ARROW",
        "TYPE_BOOL",
    ]


def test_accepts_higher_order_program():
    source = """
    let compose: ((Int -> Int), (Int -> Int)) -> Int -> Int =
      fun (f: Int -> Int, g: Int -> Int) -> Int -> Int =>
        fun (x: Int) -> Int => f(g(x))
    in
    let inc = fun (n: Int) -> Int => n + 1 in
    let twice = compose(inc, inc) in
    twice(10)
    """
    assert format_type(check_source(source)) == "Int"


def test_accepts_if_and_let_inference():
    source = "let value = if true then 10 else 20 in value + 1"
    assert format_type(check_source(source)) == "Int"


def test_accepts_bool_function_boundary():
    source = """
    let choose = fun (flag: Bool) -> Int => if flag then 1 else 2 in
    choose(false)
    """
    assert format_type(check_source(source)) == "Int"


def test_rejects_arithmetic_mismatch():
    with pytest.raises(TypeDiagnosticError, match=r"operator \+ requires Int operands"):
        check_source("true + 1")


def test_rejects_non_bool_condition():
    with pytest.raises(TypeDiagnosticError, match=r"if condition must be Bool, got Int"):
        check_source("if 1 then 2 else 3")


def test_rejects_branch_mismatch():
    with pytest.raises(TypeDiagnosticError, match=r"if branches must have same type, got Int and Bool"):
        check_source("if true then 1 else false")


def test_rejects_call_arity_mismatch():
    source = "let add = fun (x: Int, y: Int) -> Int => x + y in add(1)"
    with pytest.raises(TypeDiagnosticError, match=r"expected 2 arguments, got 1"):
        check_source(source)


def test_rejects_argument_type_mismatch():
    source = "let choose = fun (flag: Bool) -> Int => if flag then 1 else 2 in choose(1)"
    with pytest.raises(TypeDiagnosticError, match=r"argument 1 expected Bool, got Int"):
        check_source(source)


def test_rejects_wrong_return_type():
    source = "fun (flag: Bool) -> Bool => if flag then 1 else 0"
    with pytest.raises(TypeDiagnosticError, match=r"function return expected Bool, got Int"):
        check_source(source)


def test_rejects_unbound_name():
    with pytest.raises(TypeDiagnosticError, match=r"unbound name 'missing_name'"):
        check_source("missing_name")


def test_requires_parameter_annotation():
    with pytest.raises(TypeDiagnosticError, match=r"parameter 'x' requires a type annotation"):
        check_source("fun (x) -> Int => x")


def test_syntax_errors_include_location():
    with pytest.raises(SyntaxDiagnosticError, match=r"1:10: expected 'in' after let binding"):
        check_source("let x = 1")

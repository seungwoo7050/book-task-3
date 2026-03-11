from __future__ import annotations

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
    Param,
    TypeExpr,
    UnaryOp,
)
from .diagnostics import Diagnostic, SyntaxDiagnosticError
from .lexer import tokenize_source
from .tokens import Token


PRECEDENCE = {
    "OR": 1,
    "AND": 2,
    "EQEQ": 3,
    "NOTEQ": 3,
    "LT": 4,
    "LTE": 4,
    "GT": 4,
    "GTE": 4,
    "PLUS": 5,
    "MINUS": 5,
    "STAR": 6,
    "SLASH": 6,
}


BINARY_OPERATOR = {
    "OR": "or",
    "AND": "and",
    "EQEQ": "==",
    "NOTEQ": "!=",
    "LT": "<",
    "LTE": "<=",
    "GT": ">",
    "GTE": ">=",
    "PLUS": "+",
    "MINUS": "-",
    "STAR": "*",
    "SLASH": "/",
}


UNARY_OPERATOR = {
    "MINUS": "-",
    "NOT": "not",
}


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.index = 0

    def parse(self) -> Expr:
        expression = self._parse_expression()
        self._expect("EOF", "expected end of input")
        return expression

    def _parse_expression(self, min_precedence: int = 0) -> Expr:
        left = self._parse_prefix()
        left = self._parse_postfix(left)
        while True:
            token = self._current()
            precedence = PRECEDENCE.get(token.kind)
            if precedence is None or precedence < min_precedence:
                break
            operator = self._advance()
            right = self._parse_expression(precedence + 1)
            left = BinaryOp(BINARY_OPERATOR[operator.kind], left, right)
        return left

    def _parse_prefix(self) -> Expr:
        token = self._current()
        if token.kind == "LET":
            return self._parse_let()
        if token.kind == "IF":
            return self._parse_if()
        if token.kind == "FUN":
            return self._parse_fun()
        if token.kind in UNARY_OPERATOR:
            operator = self._advance()
            operand = self._parse_expression(7)
            return UnaryOp(UNARY_OPERATOR[operator.kind], operand)
        return self._parse_primary()

    def _parse_primary(self) -> Expr:
        token = self._current()
        if token.kind == "INTEGER":
            self._advance()
            return IntegerLiteral(int(token.lexeme))
        if token.kind == "TRUE":
            self._advance()
            return BooleanLiteral(True)
        if token.kind == "FALSE":
            self._advance()
            return BooleanLiteral(False)
        if token.kind == "IDENTIFIER":
            self._advance()
            return Identifier(token.lexeme)
        if token.kind == "LPAREN":
            self._advance()
            expression = self._parse_expression()
            self._expect("RPAREN", "expected ')' after expression")
            return expression
        raise self._error("expected expression", token)

    def _parse_postfix(self, expression: Expr) -> Expr:
        while self._match("LPAREN"):
            arguments: list[Expr] = []
            if not self._check("RPAREN"):
                while True:
                    arguments.append(self._parse_expression())
                    if not self._match("COMMA"):
                        break
            self._expect("RPAREN", "expected ')' after arguments")
            expression = CallExpr(expression, tuple(arguments))
        return expression

    def _parse_let(self) -> Expr:
        self._expect("LET", "expected 'let'")
        name = self._expect("IDENTIFIER", "expected binding name")
        annotation = None
        if self._match("COLON"):
            annotation = self._parse_type()
        self._expect("EQUAL", "expected '=' in let binding")
        value = self._parse_expression()
        self._expect("IN", "expected 'in' after let binding")
        body = self._parse_expression()
        return LetExpr(name.lexeme, annotation, value, body)

    def _parse_if(self) -> Expr:
        self._expect("IF", "expected 'if'")
        condition = self._parse_expression()
        self._expect("THEN", "expected 'then' after condition")
        then_branch = self._parse_expression()
        self._expect("ELSE", "expected 'else' after then branch")
        else_branch = self._parse_expression()
        return IfExpr(condition, then_branch, else_branch)

    def _parse_fun(self) -> Expr:
        self._expect("FUN", "expected 'fun'")
        self._expect("LPAREN", "expected '(' after 'fun'")
        params: list[Param] = []
        if not self._check("RPAREN"):
            while True:
                param_name = self._expect("IDENTIFIER", "expected parameter name")
                annotation = None
                if self._match("COLON"):
                    annotation = self._parse_type()
                params.append(Param(param_name.lexeme, annotation))
                if not self._match("COMMA"):
                    break
        self._expect("RPAREN", "expected ')' after parameters")
        self._expect("TYPE_ARROW", "expected '->' before return type")
        return_annotation = self._parse_type()
        self._expect("FAT_ARROW", "expected '=>' before function body")
        body = self._parse_expression()
        return FunExpr(tuple(params), return_annotation, body)

    def _parse_type(self) -> TypeExpr:
        head, grouped = self._parse_type_head()
        if self._match("TYPE_ARROW"):
            params = grouped if grouped is not None else [head]
            return FunctionType(tuple(params), self._parse_type())
        if grouped is not None:
            token = self._current()
            raise self._error("multi-parameter type list must be followed by '->'", token)
        return head

    def _parse_type_head(self) -> tuple[TypeExpr, list[TypeExpr] | None]:
        token = self._current()
        if self._match("TYPE_INT"):
            return IntType(), None
        if self._match("TYPE_BOOL"):
            return BoolType(), None
        if self._match("LPAREN"):
            if self._match("RPAREN"):
                return IntType(), []
            types = [self._parse_type()]
            if self._match("COMMA"):
                types.append(self._parse_type())
                while self._match("COMMA"):
                    types.append(self._parse_type())
                self._expect("RPAREN", "expected ')' after type list")
                return types[0], types
            self._expect("RPAREN", "expected ')' after type")
            return types[0], None
        raise self._error("expected type annotation", token)

    def _current(self) -> Token:
        return self.tokens[self.index]

    def _advance(self) -> Token:
        token = self.tokens[self.index]
        self.index += 1
        return token

    def _match(self, kind: str) -> bool:
        if self._check(kind):
            self.index += 1
            return True
        return False

    def _check(self, kind: str) -> bool:
        return self._current().kind == kind

    def _expect(self, kind: str, message: str) -> Token:
        if self._check(kind):
            return self._advance()
        raise self._error(message, self._current())

    def _error(self, message: str, token: Token) -> SyntaxDiagnosticError:
        return SyntaxDiagnosticError(Diagnostic(message, token.line, token.column))


def parse_source(source: str) -> Expr:
    return Parser(tokenize_source(source)).parse()

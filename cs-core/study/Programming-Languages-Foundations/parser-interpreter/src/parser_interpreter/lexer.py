from __future__ import annotations

from .diagnostics import Diagnostic, SyntaxDiagnosticError
from .tokens import KEYWORDS, Token


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while self._current() is not None:
            char = self._current()
            if char in " \t\r":
                self._advance()
                continue
            if char == "\n":
                self._advance_line()
                continue
            if char.isdigit():
                tokens.append(self._integer())
                continue
            if char.isalpha() or char == "_":
                tokens.append(self._identifier_or_keyword())
                continue
            tokens.append(self._punctuation())
        tokens.append(Token("EOF", "", self.line, self.column))
        return tokens

    def _integer(self) -> Token:
        line = self.line
        column = self.column
        start = self.index
        while self._current() is not None and self._current().isdigit():
            self._advance()
        return Token("INTEGER", self.source[start:self.index], line, column)

    def _identifier_or_keyword(self) -> Token:
        line = self.line
        column = self.column
        start = self.index
        while self._current() is not None and (self._current().isalnum() or self._current() == "_"):
            self._advance()
        lexeme = self.source[start:self.index]
        return Token(KEYWORDS.get(lexeme, "IDENTIFIER"), lexeme, line, column)

    def _punctuation(self) -> Token:
        line = self.line
        column = self.column
        current = self._current()
        next_char = self._peek()
        pair = (current or "") + (next_char or "")
        if pair == "->":
            self._advance()
            self._advance()
            return Token("TYPE_ARROW", "->", line, column)
        if pair == "=>":
            self._advance()
            self._advance()
            return Token("FAT_ARROW", "=>", line, column)
        if pair == "==":
            self._advance()
            self._advance()
            return Token("EQEQ", "==", line, column)
        if pair == "!=":
            self._advance()
            self._advance()
            return Token("NOTEQ", "!=", line, column)
        if pair == "<=":
            self._advance()
            self._advance()
            return Token("LTE", "<=", line, column)
        if pair == ">=":
            self._advance()
            self._advance()
            return Token("GTE", ">=", line, column)

        single_tokens = {
            "(": "LPAREN",
            ")": "RPAREN",
            ",": "COMMA",
            ":": "COLON",
            "=": "EQUAL",
            "+": "PLUS",
            "-": "MINUS",
            "*": "STAR",
            "/": "SLASH",
            "<": "LT",
            ">": "GT",
        }
        if current in single_tokens:
            self._advance()
            return Token(single_tokens[current], current, line, column)
        raise SyntaxDiagnosticError(Diagnostic(f"unexpected character '{current}'", line, column))

    def _current(self) -> str | None:
        if self.index >= len(self.source):
            return None
        return self.source[self.index]

    def _peek(self) -> str | None:
        if self.index + 1 >= len(self.source):
            return None
        return self.source[self.index + 1]

    def _advance(self) -> None:
        self.index += 1
        self.column += 1

    def _advance_line(self) -> None:
        self.index += 1
        self.line += 1
        self.column = 1


def tokenize_source(source: str) -> list[Token]:
    return Lexer(source).tokenize()

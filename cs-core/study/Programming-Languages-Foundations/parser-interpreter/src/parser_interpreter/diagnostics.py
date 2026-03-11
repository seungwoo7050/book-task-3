from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Diagnostic:
    message: str
    line: int
    column: int

    def format(self) -> str:
        if self.line <= 0 or self.column <= 0:
            return self.message
        return f"{self.line}:{self.column}: {self.message}"


class ParserInterpreterError(Exception):
    def __init__(self, diagnostic: Diagnostic) -> None:
        self.diagnostic = diagnostic
        super().__init__(diagnostic.format())


class SyntaxDiagnosticError(ParserInterpreterError):
    pass


class RuntimeDiagnosticError(ParserInterpreterError):
    pass

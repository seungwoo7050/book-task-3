from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    kind: str
    lexeme: str
    line: int
    column: int


KEYWORDS = {
    "let": "LET",
    "in": "IN",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "fun": "FUN",
    "true": "TRUE",
    "false": "FALSE",
    "not": "NOT",
    "and": "AND",
    "or": "OR",
    "Int": "TYPE_INT",
    "Bool": "TYPE_BOOL",
}

from __future__ import annotations

from dataclasses import dataclass, field

from .diagnostics import Diagnostic, RuntimeDiagnosticError


@dataclass
class Environment:
    values: dict[str, object] = field(default_factory=dict)
    parent: "Environment | None" = None

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def lookup(self, name: str) -> object:
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        raise RuntimeDiagnosticError(Diagnostic(f"unbound name '{name}'", 0, 0))

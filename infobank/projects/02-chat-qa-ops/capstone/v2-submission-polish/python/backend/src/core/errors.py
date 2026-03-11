from __future__ import annotations


class DependencyUnavailableError(RuntimeError):
    def __init__(self, component: str, message: str):
        super().__init__(message)
        self.component = component
        self.message = message

    def to_dict(self) -> dict[str, str]:
        return {
            "error_code": "DEPENDENCY_UNAVAILABLE",
            "message": self.message,
            "component": self.component,
        }

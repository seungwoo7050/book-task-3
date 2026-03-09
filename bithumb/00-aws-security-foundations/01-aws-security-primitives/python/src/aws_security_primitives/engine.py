from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
from typing import Any


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


@dataclass(slots=True)
class StatementResult:
    sid: str
    effect: str
    matched: bool
    reason: str


@dataclass(slots=True)
class Decision:
    allowed: bool
    reason: str
    matches: list[StatementResult]


def _matches(patterns: list[str], actual: str) -> bool:
    return any(fnmatchcase(actual, pattern) for pattern in patterns)


def evaluate_policy(policy: dict[str, Any], request: dict[str, str]) -> Decision:
    statements = _as_list(policy.get("Statement", []))
    normalized: list[dict[str, Any]]
    if isinstance(policy.get("Statement"), list):
        normalized = [dict(item) for item in policy["Statement"]]
    else:
        normalized = [dict(policy["Statement"])]

    results: list[StatementResult] = []
    deny_match = False
    allow_match = False

    for index, statement in enumerate(normalized, start=1):
        sid = str(statement.get("Sid", f"Statement{index}"))
        actions = _as_list(statement.get("Action", "*"))
        resources = _as_list(statement.get("Resource", "*"))
        action_match = _matches(actions, request["Action"])
        resource_match = _matches(resources, request["Resource"])
        matched = action_match and resource_match

        if matched:
            reason = "action/resource matched"
            effect = str(statement.get("Effect", "Deny"))
            if effect == "Deny":
                deny_match = True
            elif effect == "Allow":
                allow_match = True
        else:
            missing_parts: list[str] = []
            if not action_match:
                missing_parts.append("action mismatch")
            if not resource_match:
                missing_parts.append("resource mismatch")
            reason = ", ".join(missing_parts)
            effect = str(statement.get("Effect", "Deny"))
        results.append(StatementResult(sid=sid, effect=effect, matched=matched, reason=reason))

    if deny_match:
        return Decision(allowed=False, reason="explicit deny matched", matches=results)
    if allow_match:
        return Decision(allowed=True, reason="at least one allow matched", matches=results)
    return Decision(allowed=False, reason="no allow statement matched", matches=results)


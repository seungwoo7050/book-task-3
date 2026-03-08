from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from core.types import RuleResult


@dataclass
class RuleDefinition:
    rule_id: str
    rule_type: str
    severity: str
    failure_type: str
    pattern: str | None = None
    trigger: str | None = None
    required: str | None = None



def load_rules(rules_dir: str | Path) -> list[RuleDefinition]:
    path = Path(rules_dir)
    items: list[RuleDefinition] = []
    for file in sorted(path.glob("*.yaml")):
        raw = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
        for rule in raw.get("rules", []):
            items.append(
                RuleDefinition(
                    rule_id=rule["id"],
                    rule_type=rule["type"],
                    severity=rule["severity"],
                    failure_type=rule["failure_type"],
                    pattern=rule.get("pattern"),
                    trigger=rule.get("trigger"),
                    required=rule.get("required"),
                )
            )
    return items



def evaluate_rules(user_message: str, assistant_response: str, rules_dir: str | Path) -> list[RuleResult]:
    results: list[RuleResult] = []
    rules = load_rules(rules_dir)
    combined = f"{user_message}\n{assistant_response}"

    for rule in rules:
        matched = False
        evidence = ""

        if rule.rule_type in {"forbidden_pattern", "pii_detection"} and rule.pattern:
            matcher = re.search(rule.pattern, assistant_response)
            matched = matcher is not None
            evidence = matcher.group(0) if matcher else ""
        elif rule.rule_type == "mandatory_inclusion" and rule.trigger and rule.required:
            trigger_hit = re.search(rule.trigger, combined) is not None
            if trigger_hit:
                required_hit = re.search(rule.required, assistant_response) is not None
                matched = not required_hit
                evidence = assistant_response if matched else ""

        if matched:
            results.append(
                RuleResult(
                    rule_id=rule.rule_id,
                    severity=rule.severity,
                    failure_type=rule.failure_type,
                    matched=True,
                    evidence=evidence,
                    message=f"{rule.rule_id} matched",
                )
            )

    return results



def has_critical_rule(results: list[RuleResult]) -> bool:
    return any(item.severity == "critical" and item.matched for item in results)

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


HIGH_RISK_ACTIONS = {
    "iam:PassRole",
    "iam:CreatePolicyVersion",
    "iam:AttachUserPolicy",
    "iam:PutUserPolicy",
    "sts:AssumeRole",
}
READ_ONLY_PREFIXES = ("s3:Get", "s3:List", "ec2:Describe", "iam:Get", "iam:List")


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


@dataclass(slots=True)
class Finding:
    source: str
    control_id: str
    severity: str
    resource_type: str
    resource_id: str
    title: str
    evidence_ref: str


def analyze_policy(policy: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    statements = policy.get("Statement", [])
    if not isinstance(statements, list):
        statements = [statements]

    for index, statement in enumerate(statements, start=1):
        sid = str(statement.get("Sid", f"Statement{index}"))
        effect = str(statement.get("Effect", "Deny"))
        if effect != "Allow":
            continue
        actions = _as_list(statement.get("Action", []))
        resources = _as_list(statement.get("Resource", []))

        if "*" in actions:
            findings.append(
                Finding(
                    source="iam-policy",
                    control_id="IAM-001",
                    severity="HIGH",
                    resource_type="iam-policy",
                    resource_id=sid,
                    title="Policy allows every action",
                    evidence_ref=sid,
                )
            )

        if "*" in resources and any(not action.startswith(READ_ONLY_PREFIXES) for action in actions):
            findings.append(
                Finding(
                    source="iam-policy",
                    control_id="IAM-002",
                    severity="HIGH",
                    resource_type="iam-policy",
                    resource_id=sid,
                    title="Policy applies to every resource",
                    evidence_ref=sid,
                )
            )

        if HIGH_RISK_ACTIONS.intersection(actions):
            findings.append(
                Finding(
                    source="iam-policy",
                    control_id="IAM-003",
                    severity="HIGH",
                    resource_type="iam-policy",
                    resource_id=sid,
                    title="Policy contains privilege escalation actions",
                    evidence_ref=sid,
                )
            )

    return findings


def findings_as_dicts(findings: list[Finding]) -> list[dict[str, str]]:
    return [asdict(finding) for finding in findings]


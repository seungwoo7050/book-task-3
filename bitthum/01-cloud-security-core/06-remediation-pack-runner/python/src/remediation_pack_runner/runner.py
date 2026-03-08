from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class RemediationPlan:
    finding_id: str
    mode: str
    summary: str
    commands_or_patch: list[str]
    status: str


def build_dry_run(finding: dict[str, Any]) -> RemediationPlan:
    control_id = str(finding["control_id"])
    resource_id = str(finding["resource_id"])
    if control_id == "CSPM-001":
        return RemediationPlan(
            finding_id=resource_id,
            mode="auto_patch_available",
            summary="Enable all public access block flags for the bucket.",
            commands_or_patch=[
                "resource \"aws_s3_bucket_public_access_block\" \"target\" {",
                "  block_public_acls       = true",
                "  block_public_policy     = true",
                "  ignore_public_acls      = true",
                "  restrict_public_buckets = true",
                "}",
            ],
            status="pending_approval",
        )
    if control_id == "CSPM-002":
        return RemediationPlan(
            finding_id=resource_id,
            mode="manual_approval_required",
            summary="Narrow exposed ingress CIDRs and remove public SSH/RDP access.",
            commands_or_patch=[
                "terraform: replace 0.0.0.0/0 with a trusted corporate CIDR",
                "aws ec2 revoke-security-group-ingress --group-id <sg-id> --protocol tcp --port 22 --cidr 0.0.0.0/0",
            ],
            status="pending_approval",
        )
    return RemediationPlan(
        finding_id=resource_id,
        mode="manual_review",
        summary="Review the finding and apply a least-privilege remediation.",
        commands_or_patch=[
            "open a change request",
            "document approver and rollback steps",
        ],
        status="pending_approval",
    )


def approve(plan: RemediationPlan, approved_by: str) -> RemediationPlan:
    return RemediationPlan(
        finding_id=plan.finding_id,
        mode=plan.mode,
        summary=f"{plan.summary} Approved by {approved_by}.",
        commands_or_patch=plan.commands_or_patch,
        status="approved",
    )


def as_dict(plan: RemediationPlan) -> dict[str, Any]:
    return asdict(plan)


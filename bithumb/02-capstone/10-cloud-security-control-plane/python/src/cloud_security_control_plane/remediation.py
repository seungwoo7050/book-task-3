from __future__ import annotations

from uuid import uuid4

from cloud_security_control_plane.schemas import Finding, RemediationPlan


def build_remediation(finding: Finding) -> RemediationPlan:
    if finding.control_id == "CSPM-001":
        commands = [
            "Enable block_public_acls = true",
            "Enable block_public_policy = true",
            "Enable ignore_public_acls = true",
            "Enable restrict_public_buckets = true",
        ]
        mode = "auto_patch_available"
    elif finding.control_id == "CSPM-002":
        commands = [
            "Replace 0.0.0.0/0 with a trusted corporate CIDR",
            "Prepare rollback plan before revoking ingress",
        ]
        mode = "manual_approval_required"
    else:
        commands = [
            "Review the resource and prepare a least-privilege change set",
            "Capture approver and rollback details",
        ]
        mode = "manual_review"
    return RemediationPlan(
        id=str(uuid4()),
        finding_id=finding.id,
        mode=mode,
        summary=f"Dry-run remediation for {finding.control_id}",
        commands_or_patch=commands,
        status="generated",
    )


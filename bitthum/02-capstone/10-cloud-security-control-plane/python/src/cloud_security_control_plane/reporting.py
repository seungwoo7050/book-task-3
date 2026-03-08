from __future__ import annotations

from cloud_security_control_plane.schemas import ExceptionRecord, Finding, RemediationPlan


def generate_markdown_report(
    findings: list[Finding],
    exceptions: list[ExceptionRecord],
    remediations: list[RemediationPlan],
) -> str:
    lines = [
        "# Cloud Security Control Plane Report",
        "",
        "## Findings",
    ]
    if findings:
        for finding in findings:
            lines.append(
                f"- `{finding.control_id}` `{finding.severity}` `{finding.status}` `{finding.resource_id}`: {finding.title}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Exceptions"])
    if exceptions:
        for record in exceptions:
            lines.append(
                f"- `{record.scope_id}` `{record.status}` expires `{record.expires_at.isoformat()}` reason: {record.reason}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Remediation Plans"])
    if remediations:
        for plan in remediations:
            lines.append(f"- `{plan.finding_id}` `{plan.mode}` `{plan.status}`: {plan.summary}")
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


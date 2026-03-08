from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class Finding:
    source: str
    control_id: str
    severity: str
    resource_type: str
    resource_id: str
    title: str
    evidence_ref: str


def _resources(payload: dict[str, Any]) -> list[dict[str, Any]]:
    root = payload.get("planned_values", {}).get("root_module", {})
    return list(root.get("resources", []))


def scan_plan(plan_payload: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for resource in _resources(plan_payload):
        resource_type = str(resource["type"])
        name = str(resource["name"])
        values = dict(resource.get("values", {}))

        if resource_type == "aws_s3_bucket_public_access_block":
            flags = (
                values.get("block_public_acls"),
                values.get("block_public_policy"),
                values.get("ignore_public_acls"),
                values.get("restrict_public_buckets"),
            )
            if not all(flags):
                findings.append(
                    Finding(
                        source="terraform-plan",
                        control_id="CSPM-001",
                        severity="HIGH",
                        resource_type=resource_type,
                        resource_id=str(values.get("bucket", name)),
                        title="S3 bucket does not fully block public access",
                        evidence_ref=name,
                    )
                )

        if resource_type == "aws_security_group":
            for ingress in values.get("ingress", []):
                port = int(ingress.get("from_port", -1))
                cidrs = ingress.get("cidr_blocks", [])
                if port in {22, 3389} and "0.0.0.0/0" in cidrs:
                    findings.append(
                        Finding(
                            source="terraform-plan",
                            control_id="CSPM-002",
                            severity="HIGH",
                            resource_type=resource_type,
                            resource_id=name,
                            title="Security group exposes SSH or RDP to the internet",
                            evidence_ref=name,
                        )
                    )

        if resource_type in {"aws_db_instance", "aws_ebs_volume"} and values.get("storage_encrypted") is False:
            findings.append(
                Finding(
                    source="terraform-plan",
                    control_id="CSPM-003",
                    severity="MEDIUM",
                    resource_type=resource_type,
                    resource_id=str(values.get("identifier", name)),
                    title="Resource encryption is disabled",
                    evidence_ref=name,
                )
            )
    return findings


def scan_access_keys(snapshot_payload: dict[str, Any], max_age_days: int = 90) -> list[Finding]:
    findings: list[Finding] = []
    for entry in snapshot_payload.get("access_keys", []):
        if int(entry["age_days"]) > max_age_days:
            findings.append(
                Finding(
                    source="access-key-snapshot",
                    control_id="CSPM-004",
                    severity="MEDIUM",
                    resource_type="iam-access-key",
                    resource_id=str(entry["access_key_id"]),
                    title="IAM access key age exceeds threshold",
                    evidence_ref=str(entry["user"]),
                )
            )
    return findings


def findings_as_dicts(findings: list[Finding]) -> list[dict[str, str]]:
    return [asdict(finding) for finding in findings]


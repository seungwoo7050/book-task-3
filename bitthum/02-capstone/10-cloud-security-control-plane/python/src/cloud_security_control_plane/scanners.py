from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb
import yaml

from cloud_security_control_plane.schemas import EventRecord, Finding


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _finding_id(source: str, control_id: str, resource_id: str) -> str:
    raw = f"{source}:{control_id}:{resource_id}".encode()
    return hashlib.sha1(raw).hexdigest()[:16]


def scan_iam_policy(path: Path) -> list[Finding]:
    payload = json.loads(path.read_text())
    statements = payload.get("Statement", [])
    if not isinstance(statements, list):
        statements = [statements]
    findings: list[Finding] = []
    for index, statement in enumerate(statements, start=1):
        sid = str(statement.get("Sid", f"Statement{index}"))
        effect = str(statement.get("Effect", "Deny"))
        if effect != "Allow":
            continue
        actions = statement.get("Action", [])
        resources = statement.get("Resource", [])
        if not isinstance(actions, list):
            actions = [actions]
        if not isinstance(resources, list):
            resources = [resources]
        if "*" in actions:
            findings.append(
                Finding(
                    id=_finding_id("iam-policy", "IAM-001", sid),
                    source="iam-policy",
                    control_id="IAM-001",
                    severity="HIGH",
                    resource_type="iam-policy",
                    resource_id=sid,
                    title="Policy allows every action",
                    status="open",
                    detected_at=_now(),
                    evidence_ref=sid,
                )
            )
        if "*" in resources:
            findings.append(
                Finding(
                    id=_finding_id("iam-policy", "IAM-002", sid),
                    source="iam-policy",
                    control_id="IAM-002",
                    severity="HIGH",
                    resource_type="iam-policy",
                    resource_id=sid,
                    title="Policy applies to every resource",
                    status="open",
                    detected_at=_now(),
                    evidence_ref=sid,
                )
            )
    return findings


def scan_terraform_plan(path: Path) -> list[Finding]:
    payload = json.loads(path.read_text())
    resources = payload.get("planned_values", {}).get("root_module", {}).get("resources", [])
    findings: list[Finding] = []
    for resource in resources:
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
                resource_id = str(values.get("bucket", name))
                findings.append(
                    Finding(
                        id=_finding_id("terraform-plan", "CSPM-001", resource_id),
                        source="terraform-plan",
                        control_id="CSPM-001",
                        severity="HIGH",
                        resource_type=resource_type,
                        resource_id=resource_id,
                        title="S3 bucket does not fully block public access",
                        status="open",
                        detected_at=_now(),
                        evidence_ref=name,
                    )
                )
        if resource_type == "aws_security_group":
            for ingress in values.get("ingress", []):
                if int(ingress.get("from_port", -1)) in {22, 3389} and "0.0.0.0/0" in ingress.get("cidr_blocks", []):
                    findings.append(
                        Finding(
                            id=_finding_id("terraform-plan", "CSPM-002", name),
                            source="terraform-plan",
                            control_id="CSPM-002",
                            severity="HIGH",
                            resource_type=resource_type,
                            resource_id=name,
                            title="Security group exposes SSH or RDP to the internet",
                            status="open",
                            detected_at=_now(),
                            evidence_ref=name,
                        )
                    )
        if resource_type in {"aws_db_instance", "aws_ebs_volume"} and values.get("storage_encrypted") is False:
            resource_id = str(values.get("identifier", name))
            findings.append(
                Finding(
                    id=_finding_id("terraform-plan", "CSPM-003", resource_id),
                    source="terraform-plan",
                    control_id="CSPM-003",
                    severity="MEDIUM",
                    resource_type=resource_type,
                    resource_id=resource_id,
                    title="Resource encryption is disabled",
                    status="open",
                    detected_at=_now(),
                    evidence_ref=name,
                )
            )
    return findings


def scan_k8s_manifest(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    docs = list(yaml.safe_load_all(path.read_text()))
    for document in docs:
        if not isinstance(document, dict):
            continue
        metadata = document.get("metadata", {})
        resource_id = metadata.get("name", "unknown") if isinstance(metadata, dict) else "unknown"
        spec = document.get("spec", {})
        if isinstance(spec, dict) and isinstance(spec.get("template"), dict):
            spec = spec["template"].get("spec", {})
        if not isinstance(spec, dict):
            continue
        if any(isinstance(volume, dict) and "hostPath" in volume for volume in spec.get("volumes", [])):
            findings.append(
                Finding(
                    id=_finding_id("k8s-manifest", "K8S-001", str(resource_id)),
                    source="k8s-manifest",
                    control_id="K8S-001",
                    severity="HIGH",
                    resource_type="manifest",
                    resource_id=str(resource_id),
                    title="Manifest uses hostPath volume",
                    status="open",
                    detected_at=_now(),
                    evidence_ref=str(resource_id),
                )
            )
        for container in spec.get("containers", []):
            if not isinstance(container, dict):
                continue
            image = str(container.get("image", ""))
            sc = container.get("securityContext", {})
            if not isinstance(sc, dict):
                sc = {}
            if image.endswith(":latest"):
                findings.append(
                    Finding(
                        id=_finding_id("k8s-manifest", "K8S-002", str(resource_id)),
                        source="k8s-manifest",
                        control_id="K8S-002",
                        severity="MEDIUM",
                        resource_type="manifest",
                        resource_id=str(resource_id),
                        title="Container uses latest tag",
                        status="open",
                        detected_at=_now(),
                        evidence_ref=image,
                    )
                )
            if bool(sc.get("privileged")) or int(sc.get("runAsUser", 0)) == 0:
                findings.append(
                    Finding(
                        id=_finding_id("k8s-manifest", "K8S-003", str(resource_id)),
                        source="k8s-manifest",
                        control_id="K8S-003",
                        severity="HIGH",
                        resource_type="manifest",
                        resource_id=str(resource_id),
                        title="Container security context is too broad",
                        status="open",
                        detected_at=_now(),
                        evidence_ref=image,
                    )
                )
    return findings


def ingest_cloudtrail(path: Path, lake_dir: Path) -> tuple[list[EventRecord], list[Finding]]:
    payload = json.loads(path.read_text())
    rows: list[tuple[str, str, str, str]] = []
    event_records: list[EventRecord] = []
    findings: list[Finding] = []
    for entry in payload.get("Records", []):
        if not isinstance(entry, dict):
            continue
        identity = entry.get("userIdentity", {})
        actor = identity.get("arn", "unknown") if isinstance(identity, dict) else "unknown"
        event_record = EventRecord(
            occurred_at=str(entry["eventTime"]),
            source=str(entry["eventSource"]),
            event_name=str(entry["eventName"]),
            actor=str(actor),
        )
        event_records.append(event_record)
        rows.append((event_record.occurred_at, event_record.source, event_record.event_name, event_record.actor))
        control_id = None
        title = None
        if event_record.event_name == "CreateAccessKey":
            control_id = "LAKE-001"
            title = "Detected CreateAccessKey event"
        elif event_record.event_name == "DeleteTrail":
            control_id = "LAKE-004"
            title = "Detected DeleteTrail event"
        if control_id and title:
            findings.append(
                Finding(
                    id=_finding_id("cloudtrail", control_id, f"{event_record.event_name}:{event_record.actor}"),
                    source="cloudtrail",
                    control_id=control_id,
                    severity="MEDIUM",
                    resource_type="cloudtrail-event",
                    resource_id=event_record.event_name,
                    title=title,
                    status="open",
                    detected_at=_now(),
                    evidence_ref=event_record.actor,
                )
            )

    lake_dir.mkdir(parents=True, exist_ok=True)
    db_path = lake_dir / "lake.duckdb"
    parquet_path = lake_dir / "events.parquet"
    connection = duckdb.connect(str(db_path))
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS lake_events (
            occurred_at VARCHAR,
            source VARCHAR,
            event_name VARCHAR,
            actor VARCHAR
        )
        """
    )
    connection.executemany("INSERT INTO lake_events VALUES (?, ?, ?, ?)", rows)
    connection.execute(f"COPY lake_events TO '{parquet_path}' (FORMAT PARQUET)")
    return event_records, findings


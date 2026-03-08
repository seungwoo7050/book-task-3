from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class Finding:
    source: str
    control_id: str
    severity: str
    resource_type: str
    resource_id: str
    title: str
    evidence_ref: str


def scan_manifest(manifest_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    docs = list(yaml.safe_load_all(manifest_path.read_text()))
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

        for volume in spec.get("volumes", []):
            if isinstance(volume, dict) and "hostPath" in volume:
                findings.append(
                    Finding("k8s-manifest", "K8S-001", "HIGH", "volume", str(resource_id), "hostPath volume is used", str(resource_id))
                )

        for container in spec.get("containers", []):
            if not isinstance(container, dict):
                continue
            image = str(container.get("image", ""))
            security_context = container.get("securityContext", {})
            if not isinstance(security_context, dict):
                security_context = {}

            if image.endswith(":latest"):
                findings.append(
                    Finding("k8s-manifest", "K8S-002", "MEDIUM", "container", str(resource_id), "Container uses latest tag", image)
                )
            if bool(security_context.get("privileged")):
                findings.append(
                    Finding("k8s-manifest", "K8S-003", "HIGH", "container", str(resource_id), "Privileged container is enabled", image)
                )
            if int(security_context.get("runAsUser", 0)) == 0:
                findings.append(
                    Finding("k8s-manifest", "K8S-004", "HIGH", "container", str(resource_id), "Container runs as root", image)
                )
            capabilities = security_context.get("capabilities", {})
            if isinstance(capabilities, dict) and "ALL" in capabilities.get("add", []):
                findings.append(
                    Finding("k8s-manifest", "K8S-005", "HIGH", "container", str(resource_id), "Container adds broad Linux capabilities", image)
                )
    return findings


def scan_image_metadata(image_path: Path) -> list[Finding]:
    payload = json.loads(image_path.read_text())
    findings: list[Finding] = []
    image = str(payload.get("image", "unknown"))
    if image.endswith(":latest"):
        findings.append(Finding("image-metadata", "IMG-001", "MEDIUM", "image", image, "Image uses latest tag", image))
    if bool(payload.get("run_as_root")):
        findings.append(Finding("image-metadata", "IMG-002", "HIGH", "image", image, "Image runs as root", image))
    if "ALL" in payload.get("capabilities", []):
        findings.append(Finding("image-metadata", "IMG-003", "HIGH", "image", image, "Image requests ALL capabilities", image))
    return findings


def as_dicts(findings: list[Finding]) -> list[dict[str, str]]:
    return [asdict(finding) for finding in findings]


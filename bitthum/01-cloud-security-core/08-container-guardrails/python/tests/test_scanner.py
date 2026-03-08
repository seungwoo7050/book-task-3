from pathlib import Path

from container_guardrails.scanner import scan_image_metadata, scan_manifest


def _problem_data(name: str) -> Path:
    return Path(__file__).resolve().parents[2] / "problem" / "data" / name


def test_insecure_inputs_report_expected_findings() -> None:
    findings = scan_manifest(_problem_data("insecure_k8s.yaml")) + scan_image_metadata(_problem_data("insecure_image.json"))
    controls = {finding.control_id for finding in findings}
    assert controls == {"K8S-001", "K8S-002", "K8S-003", "K8S-004", "K8S-005", "IMG-001", "IMG-002", "IMG-003"}


def test_secure_inputs_report_no_findings() -> None:
    findings = scan_manifest(_problem_data("secure_k8s.yaml")) + scan_image_metadata(_problem_data("secure_image.json"))
    assert findings == []


"""capstone용 backend defense finding을 계산하는 평가기."""

from __future__ import annotations

from typing import Any


CONTROL_META: dict[str, dict[str, str]] = {
    "OWASP-001": {
        "severity": "high",
        "attack": "SQL 또는 query structure injection 위험이 있습니다.",
        "mitigation": "parameterized query 또는 동등한 bound parameter를 사용합니다.",
    },
    "OWASP-002": {
        "severity": "high",
        "attack": "Broken access control 또는 IDOR 위험이 있습니다.",
        "mitigation": "object lookup route에서 ownership 또는 scope 검사를 강제합니다.",
    },
    "OWASP-003": {
        "severity": "high",
        "attack": "private 또는 미승인 대상에 대한 SSRF 위험이 있습니다.",
        "mitigation": "outbound target은 allowlist로 제한하고 private IP range를 차단합니다.",
    },
    "OWASP-004": {
        "severity": "medium",
        "attack": "debug stacktrace와 내부 구현이 노출될 수 있습니다.",
        "mitigation": "stacktrace를 숨기고 정제된 error envelope만 반환합니다.",
    },
    "OWASP-005": {
        "severity": "high",
        "attack": "사용자 입력 파일 경로를 통한 path traversal 위험이 있습니다.",
        "mitigation": "파일에 접근하기 전에 경로를 normalize하고 허용 범위로 제한합니다.",
    },
}


def _finding(control_id: str, evidence: str) -> dict[str, str]:
    meta = CONTROL_META[control_id]
    return {
        "control_id": control_id,
        "severity": meta["severity"],
        "attack": meta["attack"],
        "mitigation": meta["mitigation"],
        "evidence": evidence,
    }


def evaluate_case(case: dict[str, Any]) -> list[dict[str, str]]:
    surface = case["surface"]
    controls = case["controls"]
    findings: list[dict[str, str]] = []

    if surface.get("database_touched") and not controls["parameterized_queries"]:
        findings.append(_finding("OWASP-001", f"route={surface['route']}에서 database_touched=true인데 parameterized_queries가 없습니다"))

    if surface.get("object_lookup") and not controls["ownership_scope_enforced"]:
        findings.append(_finding("OWASP-002", f"route={surface['route']}에서 ownership_scope_enforced 없이 object lookup을 수행합니다"))

    if surface.get("outbound_fetch") and (not controls["outbound_allowlist"] or not controls["private_ip_blocking"]):
        missing = [
            control
            for control, enabled in [
                ("outbound_allowlist", controls["outbound_allowlist"]),
                ("private_ip_blocking", controls["private_ip_blocking"]),
            ]
            if not enabled
        ]
        findings.append(_finding("OWASP-003", f"route={surface['route']}에 누락된 SSRF control: {', '.join(missing)}"))

    if surface.get("can_raise_debug") and not controls["debug_stacktrace_hidden"]:
        findings.append(_finding("OWASP-004", f"route={surface['route']}에서 can_raise_debug=true인데 debug_stacktrace_hidden=false입니다"))

    if surface.get("file_path_input") and not controls["safe_path_normalization"]:
        findings.append(_finding("OWASP-005", f"route={surface['route']}가 safe_path_normalization 없이 파일 경로를 입력받습니다"))

    return findings


def case_control_ids(case: dict[str, Any]) -> list[str]:
    return [finding["control_id"] for finding in evaluate_case(case)]

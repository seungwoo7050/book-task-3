from __future__ import annotations

from typing import Any


CONTROL_META: dict[str, dict[str, str]] = {
    "OWASP-001": {
        "severity": "high",
        "attack": "SQL or query-structure injection",
        "mitigation": "Use parameterized queries or equivalent bound parameters.",
    },
    "OWASP-002": {
        "severity": "high",
        "attack": "Broken access control / IDOR",
        "mitigation": "Enforce ownership or scope checks on object lookup routes.",
    },
    "OWASP-003": {
        "severity": "high",
        "attack": "SSRF into private or unapproved destinations",
        "mitigation": "Restrict outbound targets with allowlists and block private IP ranges.",
    },
    "OWASP-004": {
        "severity": "medium",
        "attack": "Debug stacktrace and internal implementation disclosure",
        "mitigation": "Hide stacktraces and return sanitized error envelopes.",
    },
    "OWASP-005": {
        "severity": "high",
        "attack": "Path traversal via user-controlled file paths",
        "mitigation": "Normalize and constrain file paths before access.",
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
        findings.append(_finding("OWASP-001", f"route={surface['route']} uses database_touched=true without parameterized_queries"))

    if surface.get("object_lookup") and not controls["ownership_scope_enforced"]:
        findings.append(_finding("OWASP-002", f"route={surface['route']} looks up objects without ownership_scope_enforced"))

    if surface.get("outbound_fetch") and (not controls["outbound_allowlist"] or not controls["private_ip_blocking"]):
        missing = [
            control
            for control, enabled in [
                ("outbound_allowlist", controls["outbound_allowlist"]),
                ("private_ip_blocking", controls["private_ip_blocking"]),
            ]
            if not enabled
        ]
        findings.append(_finding("OWASP-003", f"route={surface['route']} missing SSRF controls: {', '.join(missing)}"))

    if surface.get("can_raise_debug") and not controls["debug_stacktrace_hidden"]:
        findings.append(_finding("OWASP-004", f"route={surface['route']} can_raise_debug=true and debug_stacktrace_hidden=false"))

    if surface.get("file_path_input") and not controls["safe_path_normalization"]:
        findings.append(_finding("OWASP-005", f"route={surface['route']} accepts file paths without safe_path_normalization"))

    return findings


def case_control_ids(case: dict[str, Any]) -> list[str]:
    return [finding["control_id"] for finding in evaluate_case(case)]

from __future__ import annotations

from typing import Any


CONTROL_META: dict[str, dict[str, str]] = {
    "AUTH-001": {
        "severity": "high",
        "threat": "OAuth redirect CSRF or response mix-up risk",
        "recommendation": "Require and verify OAuth state on every redirect flow.",
    },
    "AUTH-002": {
        "severity": "medium",
        "threat": "Authorization code interception risk without PKCE",
        "recommendation": "Require PKCE for public and browser-facing OAuth clients.",
    },
    "AUTH-003": {
        "severity": "high",
        "threat": "JWT validation gap can accept tokens for the wrong issuer or audience",
        "recommendation": "Pin issuer, audience, and allowed algorithms before accepting JWTs.",
    },
    "AUTH-004": {
        "severity": "high",
        "threat": "Insecure token storage or overlong access token lifetime increases theft impact",
        "recommendation": "Keep bearer tokens out of localStorage and keep access token TTL short.",
    },
    "AUTH-005": {
        "severity": "high",
        "threat": "Refresh token theft is harder to detect without rotation and reuse detection",
        "recommendation": "Rotate refresh tokens and detect replay of previously used tokens.",
    },
    "AUTH-006": {
        "severity": "high",
        "threat": "Cookie-backed state changes remain vulnerable to CSRF",
        "recommendation": "Require CSRF protection on cookie-authenticated mutation requests.",
    },
    "AUTH-007": {
        "severity": "high",
        "threat": "Plaintext recovery codes become reusable account takeover secrets if leaked",
        "recommendation": "Store recovery codes as hashed secrets and reveal them only once.",
    },
    "AUTH-008": {
        "severity": "medium",
        "threat": "Missing auth throttling leaves login and recovery surfaces open to brute force",
        "recommendation": "Throttle auth endpoints at least per account and IP together.",
    },
}


def _finding(control_id: str, evidence: str) -> dict[str, str]:
    meta = CONTROL_META[control_id]
    return {
        "control_id": control_id,
        "severity": meta["severity"],
        "threat": meta["threat"],
        "recommendation": meta["recommendation"],
        "evidence": evidence,
    }


def evaluate_scenario(scenario: dict[str, Any]) -> list[dict[str, str]]:
    flow = scenario["flow"]
    controls = scenario["controls"]
    findings: list[dict[str, str]] = []

    if flow.get("oauth_enabled") and not controls["state_required"]:
        findings.append(_finding("AUTH-001", "oauth_enabled=true and state_required=false"))

    if flow.get("oauth_enabled") and not controls["pkce_required"]:
        findings.append(_finding("AUTH-002", "oauth_enabled=true and pkce_required=false"))

    if flow.get("uses_jwt"):
        missing = [
            check
            for check, enabled in [
                ("issuer_validation", controls["issuer_validation"]),
                ("audience_validation", controls["audience_validation"]),
                ("algorithm_pinning", controls["algorithm_pinning"]),
            ]
            if not enabled
        ]
        if missing:
            findings.append(_finding("AUTH-003", "missing JWT checks: " + ", ".join(missing)))

    storage_reasons: list[str] = []
    if controls["token_storage"] in {"localStorage", "sessionStorage", "url"}:
        storage_reasons.append(f"token_storage={controls['token_storage']}")
    if int(controls["access_ttl_minutes"]) > 15:
        storage_reasons.append(f"access_ttl_minutes={controls['access_ttl_minutes']}")
    if storage_reasons:
        findings.append(_finding("AUTH-004", ", ".join(storage_reasons)))

    if flow.get("uses_refresh_token"):
        missing_refresh = [
            check
            for check, enabled in [
                ("refresh_rotation", controls["refresh_rotation"]),
                ("reuse_detection", controls["reuse_detection"]),
            ]
            if not enabled
        ]
        if missing_refresh:
            findings.append(_finding("AUTH-005", "missing refresh controls: " + ", ".join(missing_refresh)))

    if flow.get("cookie_session_mutation") and not controls["csrf_protection"]:
        findings.append(_finding("AUTH-006", "cookie_session_mutation=true and csrf_protection=false"))

    if flow.get("supports_recovery_codes") and not controls["recovery_codes_hashed"]:
        findings.append(_finding("AUTH-007", "supports_recovery_codes=true and recovery_codes_hashed=false"))

    if controls["rate_limit_mode"] == "none":
        findings.append(_finding("AUTH-008", "rate_limit_mode=none"))

    return findings


def scenario_control_ids(scenario: dict[str, Any]) -> list[str]:
    return [finding["control_id"] for finding in evaluate_scenario(scenario)]


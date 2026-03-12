"""고정된 auth control vocabulary를 finding으로 변환하는 평가기."""

from __future__ import annotations

from typing import Any


CONTROL_META: dict[str, dict[str, str]] = {
    "AUTH-001": {
        "severity": "high",
        "threat": "OAuth redirect flow에서 state가 없으면 CSRF 또는 response mix-up 위험이 열립니다.",
        "recommendation": "모든 redirect flow에서 OAuth state를 요구하고 검증합니다.",
    },
    "AUTH-002": {
        "severity": "medium",
        "threat": "PKCE가 없으면 authorization code interception 위험이 커집니다.",
        "recommendation": "public client와 browser-facing client에는 PKCE를 강제합니다.",
    },
    "AUTH-003": {
        "severity": "high",
        "threat": "JWT validation이 약하면 잘못된 issuer 또는 audience의 token을 받아들일 수 있습니다.",
        "recommendation": "JWT를 수용하기 전에 issuer, audience, allowed algorithm을 고정합니다.",
    },
    "AUTH-004": {
        "severity": "high",
        "threat": "안전하지 않은 token 저장 방식이나 과도한 access token TTL은 탈취 피해를 키웁니다.",
        "recommendation": "bearer token은 localStorage에 두지 않고 access token TTL을 짧게 유지합니다.",
    },
    "AUTH-005": {
        "severity": "high",
        "threat": "rotation과 reuse detection이 없으면 refresh token 탈취를 감지하기 어렵습니다.",
        "recommendation": "refresh token을 rotation하고 재사용된 token replay를 탐지합니다.",
    },
    "AUTH-006": {
        "severity": "high",
        "threat": "cookie 기반 상태 변경 요청은 CSRF에 계속 노출됩니다.",
        "recommendation": "cookie 인증 mutation 요청에는 CSRF 보호를 강제합니다.",
    },
    "AUTH-007": {
        "severity": "high",
        "threat": "평문 recovery code는 유출 시 재사용 가능한 account takeover 비밀값이 됩니다.",
        "recommendation": "recovery code는 hash로 저장하고 한 번만 노출합니다.",
    },
    "AUTH-008": {
        "severity": "medium",
        "threat": "auth throttling이 없으면 login과 recovery 표면이 brute force에 노출됩니다.",
        "recommendation": "auth endpoint는 최소한 account와 IP를 함께 기준으로 rate limit합니다.",
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
        findings.append(_finding("AUTH-001", "oauth_enabled=true인데 state_required=false"))

    if flow.get("oauth_enabled") and not controls["pkce_required"]:
        findings.append(_finding("AUTH-002", "oauth_enabled=true인데 pkce_required=false"))

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
            findings.append(_finding("AUTH-003", "누락된 JWT 검사: " + ", ".join(missing)))

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
            findings.append(_finding("AUTH-005", "누락된 refresh control: " + ", ".join(missing_refresh)))

    if flow.get("cookie_session_mutation") and not controls["csrf_protection"]:
        findings.append(_finding("AUTH-006", "cookie_session_mutation=true인데 csrf_protection=false"))

    if flow.get("supports_recovery_codes") and not controls["recovery_codes_hashed"]:
        findings.append(_finding("AUTH-007", "supports_recovery_codes=true인데 recovery_codes_hashed=false"))

    if controls["rate_limit_mode"] == "none":
        findings.append(_finding("AUTH-008", "rate_limit_mode=none"))

    return findings


def scenario_control_ids(scenario: dict[str, Any]) -> list[str]:
    return [finding["control_id"] for finding in evaluate_scenario(scenario)]

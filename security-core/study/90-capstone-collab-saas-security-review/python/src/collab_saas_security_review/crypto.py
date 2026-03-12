"""capstone용 crypto review finding을 계산하는 평가기."""

from __future__ import annotations

from typing import Any


CONTROL_META: dict[str, dict[str, str]] = {
    "CRYPTO-001": {
        "severity": "high",
        "risk": "shared secret 검증 없는 메시지 처리는 위변조를 허용합니다.",
        "recommendation": "token, cookie, signed state 무결성에는 HMAC-SHA256 또는 동등한 MAC를 사용합니다.",
    },
    "CRYPTO-002": {
        "severity": "medium",
        "risk": "constant-time 비교가 아니면 비밀값 비교에서 timing signal이 새어 나갈 수 있습니다.",
        "recommendation": "MAC, reset token, 기타 비밀값 비교에는 constant-time comparison을 사용합니다.",
    },
    "CRYPTO-003": {
        "severity": "high",
        "risk": "약하거나 충분히 hardening되지 않은 password KDF는 탈취된 비밀번호 재료를 더 쉽게 cracking하게 만듭니다.",
        "recommendation": "Argon2id 같은 modern password KDF를 사용하고 work factor를 문서화합니다.",
    },
    "CRYPTO-004": {
        "severity": "medium",
        "risk": "key separation이나 rotation 기준이 없으면 비밀값 하나가 유출될 때 blast radius가 커집니다.",
        "recommendation": "비밀값은 목적별로 분리하고 key family마다 rotation 경계를 문서화합니다.",
    },
}


def _finding(control_id: str, evidence: str) -> dict[str, str]:
    meta = CONTROL_META[control_id]
    return {
        "control_id": control_id,
        "severity": meta["severity"],
        "risk": meta["risk"],
        "recommendation": meta["recommendation"],
        "evidence": evidence,
    }


def evaluate_crypto_review(review: dict[str, Any]) -> list[dict[str, str]]:
    controls = review["controls"]
    findings: list[dict[str, str]] = []

    if controls["message_auth"] != "hmac-sha256":
        findings.append(_finding("CRYPTO-001", f"message_auth={controls['message_auth']}"))

    if not controls["constant_time_compare"]:
        findings.append(_finding("CRYPTO-002", "constant_time_compare=false"))

    password_reasons: list[str] = []
    if controls["password_kdf"] in {"sha256", "pbkdf2-hmac-sha1"}:
        password_reasons.append(f"password_kdf={controls['password_kdf']}")
    if not controls["password_kdf_hardened"]:
        password_reasons.append("password_kdf_hardened=false")
    if password_reasons:
        findings.append(_finding("CRYPTO-003", ", ".join(password_reasons)))

    key_reasons: list[str] = []
    if not controls["key_separation"]:
        key_reasons.append("key_separation=false")
    if not controls["rotation_defined"]:
        key_reasons.append("rotation_defined=false")
    if key_reasons:
        findings.append(_finding("CRYPTO-004", ", ".join(key_reasons)))

    return findings


def crypto_control_ids(review: dict[str, Any]) -> list[str]:
    return [finding["control_id"] for finding in evaluate_crypto_review(review)]

from __future__ import annotations

from typing import Any


CONTROL_META: dict[str, dict[str, str]] = {
    "CRYPTO-001": {
        "severity": "high",
        "risk": "Unauthenticated message handling allows tampering without shared-secret verification",
        "recommendation": "Use HMAC-SHA256 or an equivalent MAC for token, cookie, and signed-state integrity.",
    },
    "CRYPTO-002": {
        "severity": "medium",
        "risk": "Secret comparisons can leak timing signals when not performed in constant time",
        "recommendation": "Use constant-time comparison for MACs, reset tokens, and other secret values.",
    },
    "CRYPTO-003": {
        "severity": "high",
        "risk": "Weak or under-hardened password KDF makes stolen password material cheaper to crack",
        "recommendation": "Use a modern password KDF such as Argon2id and document its work factors.",
    },
    "CRYPTO-004": {
        "severity": "medium",
        "risk": "Missing key separation or rotation guidance expands blast radius when one secret leaks",
        "recommendation": "Separate secrets by purpose and document rotation boundaries for each key family.",
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

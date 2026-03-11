from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

from crypto_primitives_in_practice.primitives import (
    constant_time_compare,
    hkdf_sha256,
    hmac_sha256,
    pbkdf2_hmac_sha1,
    sha256_digest,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _decode(value: str, encoding: str) -> bytes:
    if encoding == "utf-8":
        return value.encode()
    if encoding == "hex":
        return bytes.fromhex(value)
    raise ValueError(f"unsupported encoding: {encoding}")


def _encoding(manifest: dict[str, Any], vector: dict[str, Any]) -> str:
    return str(vector.get("encoding", manifest.get("encoding", "utf-8")))


def _compute_actual_hex(primitive: str, manifest: dict[str, Any], vector: dict[str, Any]) -> str:
    encoding = _encoding(manifest, vector)

    if primitive == "sha256":
        return sha256_digest(_decode(str(vector["message"]), encoding))
    if primitive == "hmac-sha256":
        return hmac_sha256(
            _decode(str(vector["key"]), encoding),
            _decode(str(vector["message"]), encoding),
        )
    if primitive == "hkdf-sha256":
        return hkdf_sha256(
            _decode(str(vector["ikm"]), encoding),
            _decode(str(vector["salt"]), encoding),
            _decode(str(vector["info"]), encoding),
            int(vector["length"]),
        )
    if primitive == "pbkdf2-hmac-sha1":
        return pbkdf2_hmac_sha1(
            _decode(str(vector["password"]), encoding),
            _decode(str(vector["salt"]), encoding),
            int(vector["iterations"]),
            int(vector["length"]),
        )
    raise ValueError(f"unsupported primitive: {primitive}")


def check_vectors_manifest(path: Path) -> dict[str, Any]:
    manifest = load_json(path)
    primitive = str(manifest["primitive"])
    results: list[dict[str, Any]] = []

    for vector in manifest["vectors"]:
        actual_hex = _compute_actual_hex(primitive, manifest, vector)
        expected_hex = str(vector["expected_hex"]).lower()
        results.append(
            {
                "name": str(vector["name"]),
                "matched": constant_time_compare(actual_hex, expected_hex),
                "actual_hex": actual_hex,
                "expected_hex": expected_hex,
            }
        )

    passed = sum(1 for result in results if result["matched"])
    failed = len(results) - passed

    return {
        "manifest": path.name,
        "title": str(manifest.get("title", path.stem)),
        "primitive": primitive,
        "passed": passed,
        "failed": failed,
        "results": results,
    }


def demo_from_profile(path: Path) -> dict[str, Any]:
    profile = load_json(path)
    encoding = str(profile.get("encoding", "utf-8"))
    message = _decode(str(profile["message"]), encoding)
    secret = _decode(str(profile["shared_secret"]), encoding)
    password = _decode(str(profile["password"]), encoding)
    salt = _decode(str(profile["salt"]), encoding)
    ikm = _decode(str(profile["ikm"]), encoding)
    info = _decode(str(profile["info"]), encoding)

    digest_hex = sha256_digest(message)
    mac_hex = hmac_sha256(secret, message)
    pbkdf2_hex = pbkdf2_hmac_sha1(
        password,
        salt,
        int(profile["pbkdf2_iterations"]),
        int(profile["pbkdf2_length"]),
    )
    hkdf_hex = hkdf_sha256(ikm, salt, info, int(profile["hkdf_length"]))

    return {
        "profile": str(profile["profile"]),
        "hash": {
            "sha256_hex": digest_hex,
        },
        "mac": {
            "hmac_sha256_hex": mac_hex,
        },
        "kdf": {
            "pbkdf2_hmac_sha1_hex": pbkdf2_hex,
            "hkdf_sha256_hex": hkdf_hex,
            "hkdf_sha256_base64url": base64.urlsafe_b64encode(bytes.fromhex(hkdf_hex))
            .rstrip(b"=")
            .decode(),
        },
        "comparisons": {
            "hash_equals_mac": constant_time_compare(digest_hex, mac_hex),
            "mac_self_check": constant_time_compare(mac_hex, hmac_sha256(secret, message)),
        },
    }


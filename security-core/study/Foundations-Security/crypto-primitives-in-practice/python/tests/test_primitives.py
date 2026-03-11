from __future__ import annotations

from pathlib import Path

from crypto_primitives_in_practice.primitives import (
    constant_time_compare,
    hkdf_sha256,
    hmac_sha256,
    pbkdf2_hmac_sha1,
)
from crypto_primitives_in_practice.vectors import check_vectors_manifest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "problem" / "data"


def test_sha256_manifest_vectors_pass() -> None:
    result = check_vectors_manifest(DATA_DIR / "sha256_vectors.json")
    assert result["failed"] == 0


def test_hmac_manifest_vectors_pass() -> None:
    result = check_vectors_manifest(DATA_DIR / "hmac_sha256_vectors.json")
    assert result["failed"] == 0


def test_hkdf_manifest_vectors_pass() -> None:
    result = check_vectors_manifest(DATA_DIR / "hkdf_sha256_vectors.json")
    assert result["failed"] == 0


def test_pbkdf2_manifest_vectors_pass() -> None:
    result = check_vectors_manifest(DATA_DIR / "pbkdf2_hmac_sha1_vectors.json")
    assert result["failed"] == 0


def test_hmac_changes_when_key_changes() -> None:
    message = b"same message"
    first = hmac_sha256(b"key-1", message)
    second = hmac_sha256(b"key-2", message)
    assert first != second


def test_pbkdf2_changes_when_iterations_change() -> None:
    first = pbkdf2_hmac_sha1(b"password", b"salt", 1000, 32)
    second = pbkdf2_hmac_sha1(b"password", b"salt", 1001, 32)
    assert first != second


def test_hkdf_changes_when_info_changes() -> None:
    ikm = b"workspace-signing-key"
    salt = b"demo-salt-2026"
    first = hkdf_sha256(ikm, salt, b"session-token", 32)
    second = hkdf_sha256(ikm, salt, b"refresh-token", 32)
    assert first != second


def test_constant_time_compare_rejects_same_length_mismatch() -> None:
    assert constant_time_compare("aaaaaaaa", "aaaaaaab") is False


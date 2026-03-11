from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from crypto_primitives_in_practice.cli import app

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "problem" / "data"
RUNNER = CliRunner()


def test_check_vectors_cli_emits_deterministic_summary() -> None:
    result = RUNNER.invoke(app, ["check-vectors", str(DATA_DIR / "sha256_vectors.json")])
    assert result.exit_code == 0

    payload = json.loads(result.stdout)
    assert payload["manifest"] == "sha256_vectors.json"
    assert payload["primitive"] == "sha256"
    assert payload["passed"] == 3
    assert payload["failed"] == 0
    assert payload["results"][1] == {
        "name": "abc",
        "matched": True,
        "actual_hex": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        "expected_hex": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    }


def test_demo_cli_emits_deterministic_profile_output() -> None:
    result = RUNNER.invoke(app, ["demo", str(DATA_DIR / "demo_profile.json")])
    assert result.exit_code == 0

    payload = json.loads(result.stdout)
    assert payload == {
        "profile": "auth-token-ish-demo",
        "hash": {
            "sha256_hex": "4f57d7ae81a37083d36a9385395a31b0659036d27d52b08f7940cdd96ecc5c48",
        },
        "mac": {
            "hmac_sha256_hex": "68a76d599c23e7cbe38f05392bc0b8e0498caeef9562be7a7755396b5bbda01d",
        },
        "kdf": {
            "pbkdf2_hmac_sha1_hex": "63f6ad0fb1289cb3d659728ae4ddf1d3c5babef89a6426e56140a661f0002253",
            "hkdf_sha256_hex": "1c76976a4dfdfddbb6c049b10743627613b65d283f697b5633bb6948a8d89474",
            "hkdf_sha256_base64url": "HHaXak39_du2wEmxB0NidhO2XSg_aXtWM7tpSKjYlHQ",
        },
        "comparisons": {
            "hash_equals_mac": False,
            "mac_self_check": True,
        },
    }


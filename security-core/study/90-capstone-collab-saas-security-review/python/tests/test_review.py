from __future__ import annotations

from pathlib import Path

from collab_saas_security_review.auth import scenario_control_ids
from collab_saas_security_review.backend import case_control_ids
from collab_saas_security_review.crypto import crypto_control_ids
from collab_saas_security_review.dependency import triage_items
from collab_saas_security_review.review import build_review_from_path, load_json

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "problem" / "data"


def test_crypto_controls_map_to_stable_ids() -> None:
    review = load_json(DATA_DIR / "review_bundle.json")["crypto_review"]
    assert crypto_control_ids(review) == ["CRYPTO-001", "CRYPTO-002", "CRYPTO-003", "CRYPTO-004"]


def test_secure_baseline_bundle_emits_empty_review() -> None:
    review = build_review_from_path(DATA_DIR / "secure_baseline_bundle.json")
    assert review["summary"] == {
        "crypto_findings": 0,
        "auth_findings": 0,
        "backend_findings": 0,
        "dependency_items": 0,
        "remediation_items": 0,
    }
    assert review["crypto_findings"] == []
    assert review["auth_findings"] == []
    assert review["backend_findings"] == []
    assert review["dependency_items"] == []
    assert review["remediation_board"] == []


def test_review_bundle_reuses_existing_control_and_priority_vocab() -> None:
    bundle = load_json(DATA_DIR / "review_bundle.json")

    assert crypto_control_ids(bundle["crypto_review"]) == bundle["crypto_review"]["expected_control_ids"]
    assert scenario_control_ids(bundle["auth_scenarios"][0]) == bundle["auth_scenarios"][0]["expected_control_ids"]
    assert case_control_ids(bundle["backend_cases"][0]) == bundle["backend_cases"][0]["expected_control_ids"]

    comparable_items = [
        {
            "package": item["package"],
            "advisory_id": item["advisory_id"],
            "priority": item["priority"],
            "action": item["action"],
            "recommended_version": item["recommended_version"],
        }
        for item in triage_items(bundle["dependency_bundle"])
    ]
    assert comparable_items == bundle["dependency_bundle"]["expected_items"]


def test_remediation_board_sorts_by_priority_then_category() -> None:
    review = build_review_from_path(DATA_DIR / "review_bundle.json")
    board = review["remediation_board"]
    priorities = [item["priority"] for item in board]
    assert priorities == sorted(priorities, key=lambda item: {"P1": 0, "P2": 1, "P3": 2, "P4": 3}[item])

    p1_categories = [item["category"] for item in board if item["priority"] == "P1"]
    assert p1_categories[:6] == ["crypto", "crypto", "auth", "auth", "auth", "auth"]
    assert p1_categories[-2:] == ["backend", "dependency"]

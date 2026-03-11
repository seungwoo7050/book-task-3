from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from owasp_backend_mitigations.evaluator import evaluate_case


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def check_case_manifest(path: Path) -> dict[str, Any]:
    manifest = load_json(path)
    results: list[dict[str, Any]] = []

    for case in manifest["cases"]:
        findings = evaluate_case(case)
        actual_control_ids = [finding["control_id"] for finding in findings]
        expected_control_ids = list(case["expected_control_ids"])
        results.append(
            {
                "name": case["name"],
                "matched": actual_control_ids == expected_control_ids,
                "actual_control_ids": actual_control_ids,
                "expected_control_ids": expected_control_ids,
                "findings": findings,
            }
        )

    passed = sum(1 for result in results if result["matched"])
    failed = len(results) - passed

    return {
        "manifest": path.name,
        "title": manifest["title"],
        "passed": passed,
        "failed": failed,
        "cases": results,
    }


def demo_profile(path: Path) -> dict[str, Any]:
    profile = load_json(path)
    findings = evaluate_case(profile)
    return {
        "profile": profile["name"],
        "control_ids": [finding["control_id"] for finding in findings],
        "findings": findings,
    }


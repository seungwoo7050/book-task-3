from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from auth_threat_modeling.evaluator import evaluate_scenario


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def check_scenarios_manifest(path: Path) -> dict[str, Any]:
    manifest = load_json(path)
    results: list[dict[str, Any]] = []

    for scenario in manifest["scenarios"]:
        findings = evaluate_scenario(scenario)
        actual_control_ids = [finding["control_id"] for finding in findings]
        expected_control_ids = list(scenario["expected_control_ids"])
        results.append(
            {
                "name": scenario["name"],
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
        "scenarios": results,
    }


def demo_profile(path: Path) -> dict[str, Any]:
    profile = load_json(path)
    findings = evaluate_scenario(profile)
    return {
        "profile": profile["name"],
        "control_ids": [finding["control_id"] for finding in findings],
        "findings": findings,
    }


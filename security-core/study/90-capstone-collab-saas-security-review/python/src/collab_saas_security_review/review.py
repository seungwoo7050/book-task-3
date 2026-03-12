"""카테고리별 finding을 하나의 remediation board와 보고서로 조합한다."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from collab_saas_security_review.auth import evaluate_scenario
from collab_saas_security_review.backend import evaluate_case
from collab_saas_security_review.crypto import evaluate_crypto_review
from collab_saas_security_review.dependency import triage_items


PRIORITY_ORDER = {
    "P1": 0,
    "P2": 1,
    "P3": 2,
    "P4": 3,
}

CATEGORY_ORDER = {
    "crypto": 0,
    "auth": 1,
    "backend": 2,
    "dependency": 3,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _normalize_priority(severity: str) -> str:
    mapping = {
        "high": "P1",
        "medium": "P2",
        "low": "P3",
    }
    return mapping[severity]


def _build_remediation_board(
    crypto_findings: list[dict[str, Any]],
    auth_findings: list[dict[str, Any]],
    backend_findings: list[dict[str, Any]],
    dependency_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    board: list[dict[str, Any]] = []

    for finding in crypto_findings:
        board.append(
            {
                "id": f"crypto:{finding['control_id']}:{finding['source']}",
                "category": "crypto",
                "priority": _normalize_priority(finding["severity"]),
                "title": finding["risk"],
                "why_now": finding["evidence"],
                "source_refs": [f"crypto_review:{finding['source']}"],
            }
        )

    for finding in auth_findings:
        board.append(
            {
                "id": f"auth:{finding['control_id']}:{finding['source']}",
                "category": "auth",
                "priority": _normalize_priority(finding["severity"]),
                "title": finding["threat"],
                "why_now": finding["evidence"],
                "source_refs": [f"auth_scenario:{finding['source']}"],
            }
        )

    for finding in backend_findings:
        board.append(
            {
                "id": f"backend:{finding['control_id']}:{finding['source']}",
                "category": "backend",
                "priority": _normalize_priority(finding["severity"]),
                "title": finding["attack"],
                "why_now": finding["evidence"],
                "source_refs": [f"backend_case:{finding['source']}"],
            }
        )

    for item in dependency_items:
        board.append(
            {
                "id": f"dependency:{item['advisory_id']}:{item['package']}",
                "category": "dependency",
                "priority": item["priority"],
                "title": f"{item['package']} 패키지는 `{item['action']}` 조치가 필요합니다",
                "why_now": ", ".join(item["reason_codes"]),
                "source_refs": [f"dependency_bundle:{item['package']}:{item['advisory_id']}"],
            }
        )

    board.sort(key=lambda item: (PRIORITY_ORDER[item["priority"]], CATEGORY_ORDER[item["category"]]))
    return board


def build_review(bundle: dict[str, Any]) -> dict[str, Any]:
    crypto_review = bundle["crypto_review"]
    crypto_findings = [
        {
            **finding,
            "source": crypto_review["name"],
        }
        for finding in evaluate_crypto_review(crypto_review)
    ]

    auth_findings = [
        {
            **finding,
            "source": scenario["name"],
        }
        for scenario in bundle["auth_scenarios"]
        for finding in evaluate_scenario(scenario)
    ]

    backend_findings = [
        {
            **finding,
            "source": case["name"],
        }
        for case in bundle["backend_cases"]
        for finding in evaluate_case(case)
    ]

    dependency_items = triage_items(bundle["dependency_bundle"])
    remediation_board = _build_remediation_board(
        crypto_findings=crypto_findings,
        auth_findings=auth_findings,
        backend_findings=backend_findings,
        dependency_items=dependency_items,
    )

    return {
        "service": bundle["service"],
        "summary": {
            "crypto_findings": len(crypto_findings),
            "auth_findings": len(auth_findings),
            "backend_findings": len(backend_findings),
            "dependency_items": len(dependency_items),
            "remediation_items": len(remediation_board),
        },
        "crypto_findings": crypto_findings,
        "auth_findings": auth_findings,
        "backend_findings": backend_findings,
        "dependency_items": dependency_items,
        "remediation_board": remediation_board,
    }


def build_review_from_path(path: Path) -> dict[str, Any]:
    return build_review(load_json(path))


def render_markdown_report(review: dict[str, Any]) -> str:
    lines = [
        "# 서비스 요약",
        f"- 서비스 이름: `{review['service']['name']}`",
        f"- tenant model: `{review['service']['tenant_model']}`",
        f"- internet exposed: `{review['service']['internet_exposed']}`",
        f"- data sensitivity: `{review['service']['data_sensitivity']}`",
        f"- crypto finding 수: `{review['summary']['crypto_findings']}`",
        f"- auth finding 수: `{review['summary']['auth_findings']}`",
        f"- backend finding 수: `{review['summary']['backend_findings']}`",
        f"- dependency item 수: `{review['summary']['dependency_items']}`",
        f"- remediation item 수: `{review['summary']['remediation_items']}`",
        "",
        "# 암호 finding",
    ]

    if review["crypto_findings"]:
        lines.extend(
            f"- `{finding['control_id']}` {finding['risk']} ({finding['evidence']})"
            for finding in review["crypto_findings"]
        )
    else:
        lines.append("- 없음")

    lines.extend(["", "# 인증 finding"])
    if review["auth_findings"]:
        lines.extend(
            f"- `{finding['control_id']}` {finding['threat']} ({finding['evidence']})"
            for finding in review["auth_findings"]
        )
    else:
        lines.append("- 없음")

    lines.extend(["", "# 백엔드 finding"])
    if review["backend_findings"]:
        lines.extend(
            f"- `{finding['control_id']}` {finding['attack']} ({finding['evidence']})"
            for finding in review["backend_findings"]
        )
    else:
        lines.append("- 없음")

    lines.extend(["", "# 의존성 큐"])
    if review["dependency_items"]:
        lines.extend(
            f"- `{item['priority']}` `{item['package']}` -> `{item['action']}`"
            for item in review["dependency_items"]
        )
    else:
        lines.append("- 없음")

    lines.extend(["", "# 조치 보드"])
    if review["remediation_board"]:
        lines.extend(
            f"- `{item['priority']}` `{item['category']}` {item['title']}"
            for item in review["remediation_board"]
        )
    else:
        lines.append("- 없음")

    return "\n".join(lines) + "\n"


def write_artifacts(bundle: dict[str, Any], review: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    payloads: dict[str, Any] = {
        "01-service-profile.json": {
            "title": bundle["title"],
            "service": review["service"],
            "summary": review["summary"],
        },
        "02-crypto-findings.json": review["crypto_findings"],
        "03-auth-findings.json": review["auth_findings"],
        "04-backend-findings.json": review["backend_findings"],
        "05-dependency-items.json": review["dependency_items"],
        "06-remediation-board.json": review["remediation_board"],
    }

    for filename, payload in payloads.items():
        (output_dir / filename).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")

    (output_dir / "07-report.md").write_text(render_markdown_report(review))

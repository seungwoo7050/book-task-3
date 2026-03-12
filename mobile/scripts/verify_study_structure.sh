#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$ROOT_DIR" <<'PY'
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
study_dir = root / "study"

root_required = [
    root / "README.md",
    root / "docs/README.md",
    root / "docs/curriculum-map.md",
    root / "docs/junior-end-skill-bar.md",
    root / "docs/repo-improvement-roadmap.md",
    root / "docs/legacy-audit.md",
    root / "docs/path-migration-map.md",
    root / "study/README.md",
    root / "scripts/report_study_status.sh",
    root / "scripts/check_study_docs.sh",
    root / "scripts/verify_study_structure.sh",
]

stage_order = ["foundations", "architecture", "product-systems", "capstone"]
expected_stage_counts = {
    "foundations": 3,
    "architecture": 2,
    "product-systems": 3,
    "capstone": 2,
}

project_headings = [
    "## 한 줄 답",
    "## 무슨 문제를 풀었나",
    "## 내가 만든 답",
    "## 무엇이 동작하나",
    "## 검증 명령",
    "## 읽는 순서",
    "## 학습 포인트",
    "## 현재 상태",
]

problem_headings = [
    "## 문제 요약",
    "## 왜 이 문제가 커리큘럼에 필요한가",
    "## 제공 자료",
    "## 필수 요구사항",
    "## 의도적 비범위",
    "## 평가/검증 기준",
    "## 원문/출처 보존 위치",
]

status_re = re.compile(r"^Status:\s*(planned|in-progress|verified|archived)\s*$", re.MULTILINE)

missing: list[str] = []

for path in root_required:
    if not path.exists():
        missing.append(f"MISSING: {path.relative_to(root)}")

for stage in stage_order:
    stage_dir = study_dir / stage
    if not stage_dir.is_dir():
        missing.append(f"MISSING: {stage_dir.relative_to(root)}")
        continue
    if not (stage_dir / "README.md").is_file():
        missing.append(f"MISSING: {stage_dir.relative_to(root)}/README.md")

projects = sorted(study_dir.glob("*/*/README.md"))
stage_counts = {stage: 0 for stage in stage_order}

for readme in projects:
    rel = readme.relative_to(root)
    stage = rel.parts[1]
    project_dir = readme.parent
    stage_counts[stage] = stage_counts.get(stage, 0) + 1
    text = readme.read_text(encoding="utf-8")

    print(f"== {stage}/{project_dir.name} ==")

    if not status_re.search(text):
        missing.append(f"MISSING: {rel} status line")

    for heading in project_headings:
        if heading not in text:
            missing.append(f"MISSING: {rel} -> {heading}")

    required_files = [
        project_dir / "problem/README.md",
        project_dir / "problem/SOURCE-PROVENANCE.md",
        project_dir / "react-native/README.md",
        project_dir / "docs/README.md",
        project_dir / "docs/concepts/README.md",
        project_dir / "docs/references/README.md",
        project_dir / "notion/README.md",
    ]

    if stage == "capstone":
        required_files.append(project_dir / "node-server/README.md")

    for path in required_files:
        if not path.exists():
            missing.append(f"MISSING: {path.relative_to(root)}")

    problem_readme = project_dir / "problem/README.md"
    if problem_readme.exists():
        problem_text = problem_readme.read_text(encoding="utf-8")
        for heading in problem_headings:
            if heading not in problem_text:
                missing.append(f"MISSING: {problem_readme.relative_to(root)} -> {heading}")

for stage, expected_count in expected_stage_counts.items():
    actual_count = stage_counts.get(stage, 0)
    if actual_count != expected_count:
        missing.append(
            f"MISMATCH: study/{stage} project count expected {expected_count}, got {actual_count}"
        )

if missing:
    for line in missing:
        print(line)
    print("study structure verification: FAILED")
    sys.exit(1)

print("study structure verification: PASSED")
PY

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$ROOT_DIR" <<'PY'
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
study_dir = root / "study"
status_re = re.compile(r"^Status:\s*(planned|in-progress|verified|archived)\s*$", re.MULTILINE)
stage_order = ["foundations", "architecture", "product-systems", "capstone"]

counts = Counter()
by_stage: dict[str, list[tuple[str, str]]] = defaultdict(list)

for readme in sorted(study_dir.glob("*/*/README.md")):
    rel = readme.relative_to(root)
    stage = rel.parts[1]
    project = rel.parts[2]
    text = readme.read_text(encoding="utf-8")
    match = status_re.search(text)
    status = match.group(1) if match else "unknown"
    counts[status] += 1
    by_stage[stage].append((project, status))

total = sum(len(items) for items in by_stage.values())

print("Study project status summary")
print(f"root: {root}")
print(f"total projects: {total}")
print()

for status in ("verified", "in-progress", "planned", "archived", "unknown"):
    if counts[status]:
        print(f"{status}: {counts[status]}")

for stage in stage_order:
    print()
    print(stage)
    for project, status in by_stage.get(stage, []):
        print(f"  - {project}: {status}")
PY

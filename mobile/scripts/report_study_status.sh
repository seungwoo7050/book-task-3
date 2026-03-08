#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$ROOT_DIR" <<'PY'
from collections import Counter
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
study_dir = root / "study"
pattern = re.compile(r"^Status:\s*(planned|in-progress|verified|archived)\s*$", re.MULTILINE)

projects = []
counts = Counter()

for readme in sorted(study_dir.glob("*/*/README.md")):
    rel = readme.relative_to(root)
    track = rel.parts[1]
    project = rel.parts[2]
    text = readme.read_text(encoding="utf-8")
    match = pattern.search(text)
    status = match.group(1) if match else "unknown"
    counts[status] += 1
    projects.append((track, project, status))

print("Study project status summary")
print(f"root: {root}")
print()

for status in ("verified", "in-progress", "planned", "archived", "unknown"):
    if counts[status]:
        print(f"{status}: {counts[status]}")

print()
current_track = None
for track, project, status in projects:
    if track != current_track:
        if current_track is not None:
            print()
        print(track)
        current_track = track
    print(f"  - {project}: {status}")
PY

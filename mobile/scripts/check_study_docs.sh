#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "$ROOT_DIR" <<'PY'
import os
import re
import sys

root = sys.argv[1]
allowed_roots = [
    os.path.join(root, "README.md"),
    os.path.join(root, "docs"),
    os.path.join(root, "study"),
]
exclude_parts = [
    "/legacy/",
    "/node_modules/",
    "/coverage/",
]
link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
inline_code_re = re.compile(r"`[^`]*`")

bad = []

def is_allowed(path: str) -> bool:
    if path == allowed_roots[0]:
        return True
    return any(path.startswith(prefix + os.sep) for prefix in allowed_roots[1:])

for dirpath, _, filenames in os.walk(root):
    if any(part in dirpath for part in exclude_parts):
        continue
    for name in filenames:
        path = os.path.join(dirpath, name)
        if not path.endswith(".md"):
            continue
        if not is_allowed(path):
            continue
        with open(path, "r", encoding="utf-8") as fh:
            in_fence = False
            for raw in fh:
                stripped = raw.strip()
                if stripped.startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                cleaned = inline_code_re.sub("", raw.rstrip("\n"))
                for match in link_re.finditer(cleaned):
                    target = match.group(1).strip()
                    if (
                        not target
                        or target.startswith("#")
                        or "://" in target
                        or target.startswith("mailto:")
                    ):
                        continue
                    target = target.split("#", 1)[0].strip()
                    if not target:
                        continue
                    resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
                    if not os.path.exists(resolved):
                        bad.append((os.path.relpath(path, root), target))

if bad:
    print(f"broken relative links: {len(bad)}")
    for rel, target in bad:
        print(f"FAIL {rel} -> {target}")
    sys.exit(1)

print("broken relative links: 0")
PY

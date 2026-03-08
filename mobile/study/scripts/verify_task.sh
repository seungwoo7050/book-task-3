#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <task_dir>"
  exit 1
fi

TASK_DIR="$(cd "$1" && pwd)"

required_files=(
  "README.md"
  "problem/README.md"
  "problem/SOURCE-PROVENANCE.md"
  "docs/README.md"
  "docs/concepts/README.md"
  "docs/references/README.md"
  "react-native/README.md"
  "notion/00-problem-framing.md"
  "notion/01-approach-log.md"
  "notion/02-debug-log.md"
  "notion/03-retrospective.md"
  "notion/04-knowledge-index.md"
)

required_dirs=(
  "problem/code"
  "problem/data"
  "problem/script"
  "docs/concepts"
  "docs/references"
  "react-native"
  "notion"
)

missing=0

for f in "${required_files[@]}"; do
  if [[ ! -f "$TASK_DIR/$f" ]]; then
    echo "MISSING FILE: $TASK_DIR/$f"
    missing=1
  fi
done

for d in "${required_dirs[@]}"; do
  if [[ ! -d "$TASK_DIR/$d" ]]; then
    echo "MISSING DIR: $TASK_DIR/$d"
    missing=1
  fi
done

if [[ ! -f "$TASK_DIR/problem/script/verify_task.sh" && ! -f "$TASK_DIR/problem/script/README.md" ]]; then
  echo "MISSING: problem/script verify entry"
  missing=1
fi

if [[ "$missing" -ne 0 ]]; then
  echo "FAIL: study task scaffold invalid -> $TASK_DIR"
  exit 1
fi

echo "PASS: study task scaffold valid -> $TASK_DIR"

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STUDY_DIR="$ROOT_DIR/study"

root_required=(
  "$ROOT_DIR/README.md"
  "$ROOT_DIR/docs/README.md"
  "$ROOT_DIR/docs/curriculum-map.md"
  "$ROOT_DIR/docs/junior-end-skill-bar.md"
  "$ROOT_DIR/docs/repo-improvement-roadmap.md"
  "$ROOT_DIR/docs/legacy-audit.md"
  "$ROOT_DIR/study/README.md"
  "$ROOT_DIR/scripts/report_study_status.sh"
)

projects=(
  "Mobile-Foundations/navigation"
  "Mobile-Foundations/virtualized-list"
  "Mobile-Foundations/gestures"
  "React-Native-Architecture/bridge-vs-jsi"
  "React-Native-Architecture/native-modules"
  "Chat-Product-Systems/offline-sync-foundations"
  "Chat-Product-Systems/realtime-chat"
  "Chat-Product-Systems/app-distribution"
  "Incident-Ops-Capstone/incident-ops-mobile"
  "Incident-Ops-Capstone/incident-ops-mobile-client"
)

missing=0

for path in "${root_required[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "MISSING: ${path#$ROOT_DIR/}"
    missing=1
  fi
done

for project in "${projects[@]}"; do
  base="$STUDY_DIR/$project"
  echo "== $project =="

  required=(
    "$base/README.md"
    "$base/problem"
    "$base/react-native"
    "$base/docs"
    "$base/notion"
  )

  for path in "${required[@]}"; do
    if [[ ! -e "$path" ]]; then
      echo "MISSING: ${path#$ROOT_DIR/}"
      missing=1
    fi
  done

  if [[ ! -f "$base/docs/concepts/README.md" ]]; then
    echo "MISSING: ${base#$ROOT_DIR/}/docs/concepts/README.md"
    missing=1
  fi

  if [[ ! -f "$base/docs/references/README.md" ]]; then
    echo "MISSING: ${base#$ROOT_DIR/}/docs/references/README.md"
    missing=1
  fi

  if [[ "$project" == Incident-Ops-Capstone/* && ! -d "$base/node-server" ]]; then
    echo "MISSING: ${base#$ROOT_DIR/}/node-server"
    missing=1
  fi
done

if ! rg -n "^study/\\*\\*/notion/" "$ROOT_DIR/.gitignore" >/dev/null 2>&1; then
  echo "MISSING: .gitignore notion rule"
  missing=1
fi

if [[ "$missing" -ne 0 ]]; then
  echo "study structure verification: FAILED"
  exit 1
fi

echo "study structure verification: PASSED"

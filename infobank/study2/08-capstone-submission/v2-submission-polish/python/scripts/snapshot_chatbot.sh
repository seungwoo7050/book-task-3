#!/usr/bin/env bash
set -euo pipefail

COMMAND="${1:-create}"
NAME="${2:-v1-freeze}"
SNAPSHOT_ROOT="${SNAPSHOT_ROOT:-../_snapshots/chat-bot}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ABS_SNAPSHOT_ROOT="$(cd "${PROJECT_ROOT}" && mkdir -p "${SNAPSHOT_ROOT}" && cd "${SNAPSHOT_ROOT}" && pwd)"

timestamp() {
  date +"%Y%m%d-%H%M%S"
}

checksum_file() {
  local target="$1"
  (
    cd "${target}"
    find . -type f -not -name "SNAPSHOT.SHA256" -print0 \
      | sort -z \
      | xargs -0 shasum -a 256 > SNAPSHOT.SHA256
  )
}

create_snapshot() {
  local ts dest
  ts="$(timestamp)"
  dest="${ABS_SNAPSHOT_ROOT}/${NAME}-${ts}"

  mkdir -p "${dest}"
  rsync -a "${PROJECT_ROOT}/" "${dest}/" \
    --exclude ".venv/" \
    --exclude "frontend/node_modules/" \
    --exclude ".pytest_cache/" \
    --exclude ".mypy_cache/" \
    --exclude ".ruff_cache/" \
    --exclude ".benchmarks/" \
    --exclude "backend/data/*.db-shm" \
    --exclude "backend/data/*.db-wal"

  checksum_file "${dest}"
  chmod -R a-w "${dest}"

  cat <<EOF
[snapshot created]
- name: ${NAME}
- path: ${dest}
- checksum: ${dest}/SNAPSHOT.SHA256
- mode: read-only
EOF
}

list_snapshots() {
  ls -1 "${ABS_SNAPSHOT_ROOT}" | sed 's#^#- #'
}

restore_snapshot() {
  local source_name="${2:-}"
  if [[ -z "${source_name}" ]]; then
    echo "Usage: $0 restore <snapshot-folder-name>"
    exit 2
  fi

  local source="${ABS_SNAPSHOT_ROOT}/${source_name}"
  if [[ ! -d "${source}" ]]; then
    echo "snapshot not found: ${source}"
    exit 1
  fi

  local restore_path="${PROJECT_ROOT}-restore-${source_name}"
  rsync -a "${source}/" "${restore_path}/"
  chmod -R u+w "${restore_path}"

  cat <<EOF
[snapshot restored]
- source: ${source}
- restored_to: ${restore_path}
EOF
}

case "${COMMAND}" in
  create)
    create_snapshot
    ;;
  list)
    list_snapshots
    ;;
  restore)
    restore_snapshot "$@"
    ;;
  *)
    cat <<EOF
Usage:
  $0 create [name]
  $0 list
  $0 restore <snapshot-folder-name>

Env:
  SNAPSHOT_ROOT (default: ../_snapshots/chat-bot)
EOF
    exit 2
    ;;
esac

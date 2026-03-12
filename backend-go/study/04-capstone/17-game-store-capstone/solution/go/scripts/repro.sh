#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT_DIR/.repro"
TS="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="$LOG_DIR/repro-$TS.log"

mkdir -p "$LOG_DIR"

cd "$ROOT_DIR"

{
  echo "[repro] started at $(date -Iseconds)"
  echo "[repro] workdir: $ROOT_DIR"
  echo "[repro] go version: $(go version)"

  if ! docker info >/dev/null 2>&1; then
    echo "[repro] ERROR: Docker daemon is not available."
    echo "[repro] Start Docker Desktop/Engine and retry."
    exit 1
  fi

  make repro

  echo "[repro] finished at $(date -Iseconds)"
} 2>&1 | tee "$LOG_FILE"

echo "[repro] log saved: $LOG_FILE"

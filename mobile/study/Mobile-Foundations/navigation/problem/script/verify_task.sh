#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
RN_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

bash "$RN_ROOT/scripts/verify_task.sh" "$TASK_DIR"

#!/usr/bin/env bash

set -euo pipefail

SHELL_PATH=${1:?usage: run_tests.sh <shell>}
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HARNESS="$SCRIPT_DIR/../../tests/direct_shell_case.sh"
TMP_DIR="$(mktemp -d)"

cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

chmod +x "$HARNESS"

"$HARNESS" "$SHELL_PATH" basic_echo > "$TMP_DIR/basic_echo.out"
grep -q "study-shell-basic" "$TMP_DIR/basic_echo.out"

"$HARNESS" "$SHELL_PATH" bg_jobs > "$TMP_DIR/bg_jobs.out"
grep -q "Running /bin/sleep 1 &" "$TMP_DIR/bg_jobs.out"

"$HARNESS" "$SHELL_PATH" sigint > "$TMP_DIR/sigint.out"
grep -q "terminated by signal" "$TMP_DIR/sigint.out"

"$HARNESS" "$SHELL_PATH" stop_fg > "$TMP_DIR/stop_fg.out"
grep -q "stopped by signal" "$TMP_DIR/stop_fg.out"
grep -q "terminated by signal" "$TMP_DIR/stop_fg.out"

echo "C shlab tests passed"

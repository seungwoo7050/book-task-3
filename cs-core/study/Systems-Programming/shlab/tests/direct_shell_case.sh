#!/usr/bin/env bash

set -euo pipefail

SHELL_PATH=${1:?usage: direct_shell_case.sh <shell> <case>}
CASE_NAME=${2:?usage: direct_shell_case.sh <shell> <case>}

if [[ "$SHELL_PATH" != /* ]]; then
    SHELL_PATH="$(cd "$(dirname "$SHELL_PATH")" && pwd)/$(basename "$SHELL_PATH")"
fi

TMP_DIR="$(mktemp -d)"
SHELL_PID=""
INPUT_FD_OPEN=0

cleanup() {
    if [[ "$INPUT_FD_OPEN" -eq 1 ]]; then
        exec 3>&-
    fi
    if [[ -n "$SHELL_PID" ]] && kill -0 "$SHELL_PID" 2>/dev/null; then
        kill "$SHELL_PID" 2>/dev/null || true
        wait "$SHELL_PID" 2>/dev/null || true
    fi
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

mkfifo "$TMP_DIR/in"
"$SHELL_PATH" -p < "$TMP_DIR/in" > "$TMP_DIR/out" 2>&1 &
SHELL_PID=$!

exec 3> "$TMP_DIR/in"
INPUT_FD_OPEN=1

case "$CASE_NAME" in
basic_echo)
    printf '/bin/echo study-shell-basic\n' >&3
    printf 'quit\n' >&3
    ;;
bg_jobs)
    printf '/bin/sleep 1\n' >&3
    printf '/bin/sleep 1 &\n' >&3
    printf 'jobs\n' >&3
    sleep 2
    printf 'quit\n' >&3
    ;;
sigint)
    printf '/bin/sleep 5\n' >&3
    sleep 1
    kill -INT "$SHELL_PID"
    sleep 1
    printf 'quit\n' >&3
    ;;
stop_fg)
    printf '/bin/sleep 5\n' >&3
    sleep 1
    kill -TSTP "$SHELL_PID"
    sleep 1
    printf 'fg %%1\n' >&3
    sleep 1
    kill -INT "$SHELL_PID"
    sleep 1
    printf 'quit\n' >&3
    ;;
*)
    echo "unknown case: $CASE_NAME" >&2
    exit 1
    ;;
esac

exec 3>&-
INPUT_FD_OPEN=0
wait "$SHELL_PID"
cat "$TMP_DIR/out"

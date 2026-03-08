#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$BASE_DIR/../../../.." && pwd)"
DOCKER_IMAGE="${DOCKER_IMAGE:-csapp-official-linux-amd64}"
HEX2RAW="$BASE_DIR/official/target1/hex2raw"
PHASE=${1:?Usage: run_attack.sh <1|2|3|4|5>}

if [ "$PHASE" -le 3 ]; then
    TARGET="$BASE_DIR/official/target1/ctarget"
else
    TARGET="$BASE_DIR/official/target1/rtarget"
fi

EXPLOIT="$BASE_DIR/data/phase${PHASE}.txt"

if [ ! -f "$TARGET" ]; then
    echo "Error: target binary not found at $TARGET"
    echo "Run 'make restore-official' first."
    exit 1
fi
if [ ! -f "$HEX2RAW" ]; then
    echo "Error: hex2raw not found at $HEX2RAW"
    exit 1
fi
if [ ! -f "$EXPLOIT" ]; then
    echo "Error: exploit file not found at $EXPLOIT"
    exit 1
fi

chmod +x "$TARGET" "$HEX2RAW"
DOCKER_FLAGS=(--rm --platform linux/amd64 -v "$REPO_ROOT:$REPO_ROOT" -w "$BASE_DIR")
if [ -t 0 ] && [ -t 1 ]; then
    DOCKER_FLAGS+=(-it)
else
    DOCKER_FLAGS+=(-i)
fi

docker run "${DOCKER_FLAGS[@]}" "$DOCKER_IMAGE" bash -lc \
    "'$HEX2RAW' < '$EXPLOIT' | '$TARGET' -q"

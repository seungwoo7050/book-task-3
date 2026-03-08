#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$BASE_DIR/../../../.." && pwd)"
DOCKER_IMAGE="${DOCKER_IMAGE:-csapp-official-linux-amd64}"
BOMB="$BASE_DIR/official/bomb/bomb"
SOLUTION="$BASE_DIR/data/solutions.txt"

if [ ! -f "$BOMB" ]; then
    echo "Error: Bomb binary not found at $BOMB"
    echo "Run 'make restore-official' first."
    exit 1
fi

chmod +x "$BOMB"

DOCKER_FLAGS=(--rm --platform linux/amd64 -v "$REPO_ROOT:$REPO_ROOT" -w "$BASE_DIR")
if [ -t 0 ] && [ -t 1 ]; then
    DOCKER_FLAGS+=(-it)
else
    DOCKER_FLAGS+=(-i)
fi

if [ "${1:-}" = "--gdb" ]; then
    docker run "${DOCKER_FLAGS[@]}" "$DOCKER_IMAGE" bash -lc \
        "gdb -ex 'break explode_bomb' -ex 'run $SOLUTION' '$BOMB'"
else
    docker run "${DOCKER_FLAGS[@]}" "$DOCKER_IMAGE" bash -lc "'$BOMB' '$SOLUTION'"
fi

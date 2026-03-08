#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
PROXY_BIN=${1:-}

if [[ -z "$PROXY_BIN" ]]; then
    echo "usage: driver.sh <proxy-binary>" >&2
    exit 1
fi

bash "$ROOT_DIR/tests/run_proxy_tests.sh" "$PROXY_BIN"

#!/usr/bin/env bash
# Verify completeness of 802.11 Wireless lab answers
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
TRACK_DIR="$(cd "$LAB_DIR/.." && pwd)"

python3 "$TRACK_DIR/tools/verify_packet_lab.py" "$LAB_DIR"

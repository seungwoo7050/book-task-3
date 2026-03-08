#!/usr/bin/env bash
# grade.sh — Run dlc + btest and print a score summary for Data Lab.
#
# Usage:
#   bash script/grade.sh          (from problem/ directory)
#
# Exit code: 0 if all puzzles pass, 1 otherwise.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_DIR="$BASE_DIR/code"
DLC="$CODE_DIR/dlc"
BITS="$CODE_DIR/bits.c"
BTEST="$BASE_DIR/btest"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

echo "======================================="
echo "  Data Lab Grading Script"
echo "======================================="
echo

# ── Step 1: Build ──────────────────────────────────────────────
echo -e "${YELLOW}[1/3] Building btest...${NC}"
cd "$BASE_DIR"
make clean > /dev/null 2>&1 || true
make all
echo

# ── Step 2: Check operator legality ────────────────────────────
echo -e "${YELLOW}[2/3] Checking operator legality (dlc)...${NC}"
if [ -x "$DLC" ]; then
    if $DLC "$BITS"; then
        echo -e "${GREEN}  dlc: All restrictions satisfied.${NC}"
    else
        echo -e "${RED}  dlc: VIOLATION detected. Fix illegal operators before proceeding.${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}  dlc binary not found — skipping operator check.${NC}"
    echo "  (Download dlc from the CS:APP website to enable this check.)"
fi
echo

# ── Step 3: Run btest ─────────────────────────────────────────
echo -e "${YELLOW}[3/3] Running correctness tests (btest)...${NC}"
if "$BTEST"; then
    echo
    echo -e "${GREEN}=== ALL TESTS PASSED ===${NC}"
    exit 0
else
    echo
    echo -e "${RED}=== SOME TESTS FAILED ===${NC}"
    exit 1
fi

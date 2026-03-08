#!/usr/bin/env bash
# RDT Protocol — Test Script
#
# Usage:
#   bash test_rdt.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROBLEM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_DIR="$PROBLEM_DIR/code"
SOLUTION_DIR="$PROBLEM_DIR/../python/src"

echo "========================================"
echo " RDT Protocol Test Suite"
echo "========================================"
echo ""

PASS=0
FAIL=0

# Test RDT 3.0
printf "TEST: %-40s " "RDT 3.0 completes transfer"
if OUTPUT=$(cd "$CODE_DIR" && python3 "${SOLUTION_DIR}/rdt3.py" --loss 0.2 --corrupt 0.1 2>&1); then
    STATUS=0
else
    STATUS=$?
fi
if [[ ${STATUS} -eq 0 ]] && echo "${OUTPUT}" | grep -qi "success\|complete\|delivered"; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL]"
    FAIL=$((FAIL + 1))
fi

# Test GBN
printf "TEST: %-40s " "GBN completes transfer"
if OUTPUT=$(cd "$CODE_DIR" && python3 "${SOLUTION_DIR}/gbn.py" --loss 0.2 --corrupt 0.1 --window 4 2>&1); then
    STATUS=0
else
    STATUS=$?
fi
if [[ ${STATUS} -eq 0 ]] && echo "${OUTPUT}" | grep -qi "success\|complete\|delivered"; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL]"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "========================================"
echo " Results: ${PASS} passed, ${FAIL} failed"
echo "========================================"

[[ ${FAIL} -eq 0 ]] || exit 1

#!/usr/bin/env bash
# Selective Repeat — Test Script
#
# Usage:
#   bash test_selective_repeat.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROBLEM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SOLUTION="$PROBLEM_DIR/../python/src/selective_repeat.py"

echo "========================================"
echo " Selective Repeat Test Suite"
echo "========================================"
echo ""

PASS=0
FAIL=0

printf "TEST: %-40s " "Selective Repeat completes transfer"
if OUTPUT=$(python3 "$SOLUTION" --loss 0.2 --corrupt 0.1 --window 4 2>&1); then
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

printf "TEST: %-40s " "Sender retransmits selectively"
if echo "${OUTPUT}" | grep -qi "Retransmitting seq"; then
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

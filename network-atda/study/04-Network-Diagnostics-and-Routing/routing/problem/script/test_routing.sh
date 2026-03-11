#!/usr/bin/env bash
# Distance-Vector Routing — Test Script
#
# Usage:
#   bash test_routing.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROBLEM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

SOLUTION="$PROBLEM_DIR/../python/src/dv_routing.py"
DATA_DIR="$PROBLEM_DIR/data"
PYTHON=python3

echo "========================================"
echo " Distance-Vector Routing Test Suite"
echo "========================================"
echo ""

PASS=0
FAIL=0

# --------------------------------------------------
# Test 1: Basic 3-node topology
# --------------------------------------------------
printf "TEST: %-40s " "3-node topology convergence"
OUTPUT=$("${PYTHON}" "${SOLUTION}" "${DATA_DIR}/topology.json" 2>&1) && STATUS=0 || STATUS=$?
if [[ ${STATUS} -eq 0 ]] && echo "${OUTPUT}" | grep -qi "converge"; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL]"
    FAIL=$((FAIL + 1))
fi

# Test: x→z should be cost 3 via y
printf "TEST: %-40s " "x→z shortest path = 3 via y"
if echo "${OUTPUT}" | grep -q "to z cost 3"; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL]"
    FAIL=$((FAIL + 1))
fi

# --------------------------------------------------
# Test 2: 5-node topology
# --------------------------------------------------
printf "TEST: %-40s " "5-node topology convergence"
OUTPUT5=$("${PYTHON}" "${SOLUTION}" "${DATA_DIR}/topology_5node.json" 2>&1) && STATUS=0 || STATUS=$?
if [[ ${STATUS} -eq 0 ]] && echo "${OUTPUT5}" | grep -qi "converge"; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL]"
    FAIL=$((FAIL + 1))
fi

# Test: a→e should be cost 5 (a→b:1, b→c:2, c→d:1, d→e:1)
printf "TEST: %-40s " "a→e shortest path = 5"
if echo "${OUTPUT5}" | grep -q "to e cost 5"; then
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

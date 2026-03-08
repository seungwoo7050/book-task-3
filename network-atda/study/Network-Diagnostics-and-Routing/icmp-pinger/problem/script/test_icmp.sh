#!/usr/bin/env bash
# ICMP Pinger — Test Script
#
# Usage:
#   sudo bash test_icmp.sh [host]
#
# Requires root privileges.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROBLEM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

HOST="${1:-google.com}"
SOLUTION="$PROBLEM_DIR/../python/src/icmp_pinger.py"

echo "========================================"
echo " ICMP Pinger Test Suite"
echo " Target: ${HOST}"
echo "========================================"
echo ""

PASS=0
FAIL=0

# Test: ping completes without errors
printf "TEST: %-40s " "Ping completes successfully"
OUTPUT=$(python3 "${SOLUTION}" "${HOST}" -c 4 2>&1) && STATUS=0 || STATUS=$?
if [[ ${STATUS} -eq 0 ]]; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL] Exit code: ${STATUS}"
    FAIL=$((FAIL + 1))
fi

# Test: output contains RTT values
printf "TEST: %-40s " "Output contains RTT measurements"
if echo "${OUTPUT}" | grep -qi "rtt\|ms"; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL]"
    FAIL=$((FAIL + 1))
fi

# Test: output contains statistics
printf "TEST: %-40s " "Output contains ping statistics"
if echo "${OUTPUT}" | grep -qi "packets\|loss\|statistics"; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL]"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "${OUTPUT}"
echo ""
echo "========================================"
echo " Results: ${PASS} passed, ${FAIL} failed"
echo "========================================"

[[ ${FAIL} -eq 0 ]] || exit 1

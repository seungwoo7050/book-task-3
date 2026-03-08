#!/usr/bin/env bash
# UDP Pinger — Test Script
#
# Usage:
#   bash test_pinger.sh [host] [port]
#
# The UDP pinger server must be running before executing this script.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROBLEM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

HOST="${1:-127.0.0.1}"
PORT="${2:-12000}"
SOLUTION="$PROBLEM_DIR/../python/src/udp_pinger_client.py"

echo "========================================"
echo " UDP Pinger Test Suite"
echo " Target: ${HOST}:${PORT}"
echo "========================================"
echo ""

# Run the solution and capture output
OUTPUT=$(python3 "${SOLUTION}" "${HOST}" "${PORT}" 2>&1)

echo "${OUTPUT}"
echo ""

PASS=0
FAIL=0

# Test: output contains "Ping" lines
printf "TEST: %-40s " "Output contains Ping lines"
if echo "${OUTPUT}" | grep -q "Ping"; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL]"
    FAIL=$((FAIL + 1))
fi

# Test: output contains statistics
printf "TEST: %-40s " "Output contains statistics"
if echo "${OUTPUT}" | grep -qi "packets\|loss\|RTT"; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL]"
    FAIL=$((FAIL + 1))
fi

# Test: at least one RTT is reported (some may time out)
printf "TEST: %-40s " "At least one RTT measurement"
if echo "${OUTPUT}" | grep -qi "rtt\|ms"; then
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

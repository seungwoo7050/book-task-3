#!/usr/bin/env bash
# SMTP Client — Test Script
#
# Usage:
#   bash test_smtp.sh [host] [port]
#
# A local SMTP debug server must be running:
#   python3 -m smtpd -n -c DebuggingServer localhost:1025

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROBLEM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

HOST="${1:-localhost}"
PORT="${2:-1025}"
SOLUTION="$PROBLEM_DIR/../python/src/smtp_client.py"
SENDER="test-sender@example.com"
RCPT="test-recipient@example.com"

echo "========================================"
echo " SMTP Client Test Suite"
echo " Server: ${HOST}:${PORT}"
echo "========================================"
echo ""

PASS=0
FAIL=0

# Test: solution runs without errors
printf "TEST: %-40s " "Client completes SMTP dialogue"
OUTPUT=$(python3 "${SOLUTION}" "${HOST}" "${PORT}" "${SENDER}" "${RCPT}" 2>&1) && STATUS=0 || STATUS=$?

if [[ ${STATUS} -eq 0 ]]; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL] Exit code: ${STATUS}"
    FAIL=$((FAIL + 1))
fi

# Test: output contains success message
printf "TEST: %-40s " "Output indicates success"
if echo "${OUTPUT}" | grep -qi "sent successfully\|250"; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL]"
    FAIL=$((FAIL + 1))
fi

# Test: output shows SMTP commands
printf "TEST: %-40s " "Output shows SMTP dialogue"
if echo "${OUTPUT}" | grep -qi "HELO\|MAIL FROM\|RCPT TO\|DATA\|QUIT"; then
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

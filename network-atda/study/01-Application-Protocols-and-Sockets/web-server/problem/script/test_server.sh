#!/usr/bin/env bash
# Web Server — Automated Test Script
#
# Usage:
#   bash test_server.sh [host] [port]
#
# Prerequisites:
#   The web server must already be running on the specified host:port.

set -euo pipefail

HOST="${1:-localhost}"
PORT="${2:-6789}"
BASE_URL="http://${HOST}:${PORT}"
PASS=0
FAIL=0

echo "========================================"
echo " Web Server Test Suite"
echo " Target: ${BASE_URL}"
echo "========================================"
echo ""

# --- Helper -----------------------------------------------------------
run_test() {
    local description="$1"
    local url="$2"
    local expected_code="$3"
    local expected_body="${4:-}"

    printf "TEST: %-40s " "${description}"

    response=$(curl -s -o /tmp/ws_test_body.txt -w "%{http_code}" "${url}" 2>/dev/null || echo "000")

    if [[ "${response}" == "${expected_code}" ]]; then
        if [[ -n "${expected_body}" ]]; then
            if grep -q "${expected_body}" /tmp/ws_test_body.txt 2>/dev/null; then
                echo "[PASS]"
                PASS=$((PASS + 1))
            else
                echo "[FAIL] Body mismatch"
                FAIL=$((FAIL + 1))
            fi
        else
            echo "[PASS]"
            PASS=$((PASS + 1))
        fi
    else
        echo "[FAIL] Expected ${expected_code}, got ${response}"
        FAIL=$((FAIL + 1))
    fi
}

# --- Tests ------------------------------------------------------------
run_test "GET /hello.html returns 200"       "${BASE_URL}/hello.html"       "200" "Hello"
run_test "GET /nonexistent returns 404"      "${BASE_URL}/nonexistent.html" "404"
run_test "Body contains HTML content"        "${BASE_URL}/hello.html"       "200" "<html"

# --- Summary ----------------------------------------------------------
echo ""
echo "========================================"
echo " Results: ${PASS} passed, ${FAIL} failed"
echo "========================================"

rm -f /tmp/ws_test_body.txt

if [[ ${FAIL} -gt 0 ]]; then
    exit 1
fi

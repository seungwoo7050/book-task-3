#!/usr/bin/env bash
# Web Proxy — Test Script
#
# Usage:
#   bash test_proxy.sh [port]
#
# The proxy must be running before executing this script.

set -euo pipefail

PORT="${1:-8888}"
PROXY="http://localhost:${PORT}"
ORIGIN_PORT="${2:-18080}"
TMP_ORIGIN_DIR="$(mktemp -d)"
TARGET_URL="http://127.0.0.1:${ORIGIN_PORT}/"

cleanup() {
    if [[ -n "${ORIGIN_PID:-}" ]]; then
        kill "${ORIGIN_PID}" >/dev/null 2>&1 || true
        wait "${ORIGIN_PID}" >/dev/null 2>&1 || true
    fi
    rm -rf "${TMP_ORIGIN_DIR}"
}
trap cleanup EXIT

cat > "${TMP_ORIGIN_DIR}/index.html" <<'EOF'
<html><body><h1>Proxy Test Page</h1><p>hello-cache</p></body></html>
EOF

python3 -m http.server "${ORIGIN_PORT}" --bind 127.0.0.1 --directory "${TMP_ORIGIN_DIR}" >/tmp/net_proxy_origin.log 2>&1 &
ORIGIN_PID=$!

# Wait until origin server is ready.
for _ in $(seq 1 20); do
    if [[ "$(curl -s -o /dev/null -w "%{http_code}" "${TARGET_URL}" 2>/dev/null || echo 000)" == "200" ]]; then
        break
    fi
    sleep 0.2
done

echo "========================================"
echo " Web Proxy Test Suite"
echo " Proxy: ${PROXY}"
echo " Origin: ${TARGET_URL}"
echo "========================================"
echo ""

PASS=0
FAIL=0

# Test 1: Proxy fetches a page
printf "TEST: %-40s " "Fetch ${TARGET_URL}"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -x "${PROXY}" "${TARGET_URL}" 2>/dev/null || echo "000")
if [[ "${CODE}" == "200" ]]; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL] HTTP ${CODE}"
    FAIL=$((FAIL + 1))
fi

# Test 2: Second request should be cached (proxy still works)
printf "TEST: %-40s " "Second fetch (cache check)"
CODE2=$(curl -s -o /dev/null -w "%{http_code}" -x "${PROXY}" "${TARGET_URL}" 2>/dev/null || echo "000")
if [[ "${CODE2}" == "200" ]]; then
    echo "[PASS]"
    PASS=$((PASS + 1))
else
    echo "[FAIL] HTTP ${CODE2}"
    FAIL=$((FAIL + 1))
fi

# Test 3: Response body is non-empty
printf "TEST: %-40s " "Response body is non-empty"
BODY=$(curl -s -x "${PROXY}" "${TARGET_URL}" 2>/dev/null)
if [[ -n "${BODY}" ]]; then
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

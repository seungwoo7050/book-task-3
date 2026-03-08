#!/usr/bin/env bash
# Evaluation script for 01-go-api-standard
# Starts the server and runs basic HTTP tests against it.

set -euo pipefail

BASE_URL="http://localhost:${PORT:-4000}"

echo "=== 01-go-api-standard Evaluation ==="
echo ""

# 1. Healthcheck
echo "[1/5] Testing GET /v1/healthcheck..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/v1/healthcheck")
if [ "$STATUS" = "200" ]; then
  echo "  PASS: healthcheck returned 200"
else
  echo "  FAIL: healthcheck returned $STATUS (expected 200)"
fi

# 2. Create a movie
echo "[2/5] Testing POST /v1/movies..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/v1/movies" \
  -H "Content-Type: application/json" \
  -d '{"title":"Moana","year":2016,"runtime":107,"genres":["animation","adventure"]}')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n 1)
if [ "$STATUS" = "201" ]; then
  echo "  PASS: create movie returned 201"
else
  echo "  FAIL: create movie returned $STATUS (expected 201)"
fi

# 3. Get the movie
echo "[3/5] Testing GET /v1/movies/1..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/v1/movies/1")
if [ "$STATUS" = "200" ]; then
  echo "  PASS: get movie returned 200"
else
  echo "  FAIL: get movie returned $STATUS (expected 200)"
fi

# 4. List movies
echo "[4/5] Testing GET /v1/movies..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/v1/movies")
if [ "$STATUS" = "200" ]; then
  echo "  PASS: list movies returned 200"
else
  echo "  FAIL: list movies returned $STATUS (expected 200)"
fi

# 5. Not found
echo "[5/5] Testing GET /v1/movies/9999 (not found)..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/v1/movies/9999")
if [ "$STATUS" = "404" ]; then
  echo "  PASS: not found returned 404"
else
  echo "  FAIL: not found returned $STATUS (expected 404)"
fi

echo ""
echo "=== Evaluation Complete ==="

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${PORT:-4080}"
DATABASE_URL="${DATABASE_URL:-postgres://postgres:postgres@localhost:54339/workspace_saas?sslmode=disable}"
REDIS_ADDR="${REDIS_ADDR:-localhost:6381}"
JWT_SECRET="${JWT_SECRET:-workspace-saas-secret}"
WORKER_POLL_INTERVAL="${WORKER_POLL_INTERVAL:-250ms}"
BASE_URL="http://127.0.0.1:${PORT}"
API_LOG="$(mktemp)"
WORKER_LOG="$(mktemp)"

cleanup() {
  if [[ -n "${API_PID:-}" ]]; then kill "${API_PID}" >/dev/null 2>&1 || true; fi
  if [[ -n "${WORKER_PID:-}" ]]; then kill "${WORKER_PID}" >/dev/null 2>&1 || true; fi
  rm -f "${API_LOG}" "${WORKER_LOG}"
}
trap cleanup EXIT

cd "${ROOT_DIR}"

PORT="${PORT}" DATABASE_URL="${DATABASE_URL}" REDIS_ADDR="${REDIS_ADDR}" JWT_SECRET="${JWT_SECRET}" \
  go run ./cmd/api >"${API_LOG}" 2>&1 &
API_PID=$!

DATABASE_URL="${DATABASE_URL}" REDIS_ADDR="${REDIS_ADDR}" JWT_SECRET="${JWT_SECRET}" WORKER_POLL_INTERVAL="${WORKER_POLL_INTERVAL}" \
  go run ./cmd/worker >"${WORKER_LOG}" 2>&1 &
WORKER_PID=$!

for _ in $(seq 1 40); do
  if curl -sf "${BASE_URL}/readyz" >/dev/null; then
    break
  fi
  sleep 1
done

curl -sf "${BASE_URL}/readyz" >/dev/null

SUFFIX="$(python3 - <<'PY'
import time
print(int(time.time() * 1000))
PY
)"

OWNER_EMAIL="owner-${SUFFIX}@example.com"
MEMBER_EMAIL="member-${SUFFIX}@example.com"
OWNER_PASSWORD="OwnerPass123!"
MEMBER_PASSWORD="MemberPass123!"
ORG_SLUG="workspace-${SUFFIX}"
PROJECT_KEY="OPS${SUFFIX: -4}"

register_response="$(curl -sf -X POST "${BASE_URL}/v1/auth/register-owner" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"${OWNER_EMAIL}\",\"password\":\"${OWNER_PASSWORD}\",\"display_name\":\"Owner ${SUFFIX}\",\"org_name\":\"Workspace ${SUFFIX}\",\"org_slug\":\"${ORG_SLUG}\"}")"

OWNER_ACCESS="$(python3 - <<'PY' "${register_response}"
import json, sys
print(json.loads(sys.argv[1])["access_token"])
PY
)"
OWNER_REFRESH="$(python3 - <<'PY' "${register_response}"
import json, sys
print(json.loads(sys.argv[1])["refresh_token"])
PY
)"
ORG_ID="$(python3 - <<'PY' "${register_response}"
import json, sys
print(json.loads(sys.argv[1])["memberships"][0]["organization_id"])
PY
)"

project_response="$(curl -sf -X POST "${BASE_URL}/v1/orgs/${ORG_ID}/projects" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${OWNER_ACCESS}" \
  -d "{\"name\":\"Operations\",\"project_key\":\"${PROJECT_KEY}\"}")"

PROJECT_ID="$(python3 - <<'PY' "${project_response}"
import json, sys
print(json.loads(sys.argv[1])["project"]["id"])
PY
)"

invite_response="$(curl -sf -X POST "${BASE_URL}/v1/orgs/${ORG_ID}/invitations" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${OWNER_ACCESS}" \
  -H 'Idempotency-Key: invite-smoke-1' \
  -d "{\"email\":\"${MEMBER_EMAIL}\",\"role\":\"member\"}")"

INVITE_TOKEN="$(python3 - <<'PY' "${invite_response}"
import json, sys
print(json.loads(sys.argv[1])["accept_token_preview"])
PY
)"

accept_response="$(curl -sf -X POST "${BASE_URL}/v1/invitations/accept" \
  -H 'Content-Type: application/json' \
  -d "{\"token\":\"${INVITE_TOKEN}\",\"display_name\":\"Member ${SUFFIX}\",\"password\":\"${MEMBER_PASSWORD}\"}")"

MEMBER_ACCESS="$(python3 - <<'PY' "${accept_response}"
import json, sys
print(json.loads(sys.argv[1])["access_token"])
PY
)"
MEMBER_ID="$(python3 - <<'PY' "${accept_response}"
import json, sys
print(json.loads(sys.argv[1])["user"]["id"])
PY
)"

issue_response="$(curl -sf -X POST "${BASE_URL}/v1/projects/${PROJECT_ID}/issues" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${MEMBER_ACCESS}" \
  -H 'Idempotency-Key: issue-smoke-1' \
  -d "{\"title\":\"Investigate dashboard lag\",\"description\":\"Summary endpoint needs profiling\"}")"

ISSUE_ID="$(python3 - <<'PY' "${issue_response}"
import json, sys
print(json.loads(sys.argv[1])["issue"]["id"])
PY
)"
ISSUE_VERSION="$(python3 - <<'PY' "${issue_response}"
import json, sys
print(json.loads(sys.argv[1])["issue"]["version"])
PY
)"

update_response="$(curl -sf -X PATCH "${BASE_URL}/v1/issues/${ISSUE_ID}" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${OWNER_ACCESS}" \
  -d "{\"status\":\"in_progress\",\"assignee_user_id\":\"${MEMBER_ID}\",\"version\":${ISSUE_VERSION}}")"

UPDATED_VERSION="$(python3 - <<'PY' "${update_response}"
import json, sys
print(json.loads(sys.argv[1])["issue"]["version"])
PY
)"
curl -sf -X POST "${BASE_URL}/v1/issues/${ISSUE_ID}/comments" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${MEMBER_ACCESS}" \
  -d '{"body":"Initial triage complete. Profiling next."}' >/dev/null

sleep 1

notifications_response="$(curl -sf "${BASE_URL}/v1/orgs/${ORG_ID}/notifications" \
  -H "Authorization: Bearer ${OWNER_ACCESS}")"
python3 - <<'PY' "${notifications_response}"
import json, sys
items = json.loads(sys.argv[1])["notifications"]
assert len(items) >= 1, "expected at least one notification"
PY

summary_response="$(curl -sf "${BASE_URL}/v1/orgs/${ORG_ID}/dashboard/summary" \
  -H "Authorization: Bearer ${OWNER_ACCESS}")"
python3 - <<'PY' "${summary_response}"
import json, sys
summary = json.loads(sys.argv[1])["summary"]
assert summary["projects_total"] == 1, summary
assert summary["issues_in_progress"] >= 1, summary
assert summary["unread_notifications"] >= 1, summary
PY

refresh_response="$(curl -sf -X POST "${BASE_URL}/v1/auth/refresh" \
  -H 'Content-Type: application/json' \
  -d "{\"refresh_token\":\"${OWNER_REFRESH}\"}")"
NEW_REFRESH="$(python3 - <<'PY' "${refresh_response}"
import json, sys
print(json.loads(sys.argv[1])["refresh_token"])
PY
)"

curl -sf -X POST "${BASE_URL}/v1/auth/logout" \
  -H 'Content-Type: application/json' \
  -d "{\"refresh_token\":\"${NEW_REFRESH}\"}" \
  -o /dev/null -w '%{http_code}' | grep -q '^204$'

echo "smoke scenario completed successfully"

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR="$(cd "${ROOT_DIR}/.." && pwd)"
ASSET_DIR="${PROJECT_DIR}/docs/presentation-assets/demo-2026-03-07"
PORT="${PORT:-4080}"
DATABASE_URL="${DATABASE_URL:-postgres://postgres:postgres@localhost:54339/workspace_saas?sslmode=disable}"
REDIS_ADDR="${REDIS_ADDR:-localhost:6381}"
JWT_SECRET="${JWT_SECRET:-workspace-saas-secret}"
WORKER_POLL_INTERVAL="${WORKER_POLL_INTERVAL:-250ms}"
BASE_URL="http://127.0.0.1:${PORT}"
API_LOG="${ASSET_DIR}/90-api.log"
WORKER_LOG="${ASSET_DIR}/91-worker.log"
RUN_LOG="${ASSET_DIR}/00-demo.log"

mkdir -p "${ASSET_DIR}"
rm -f "${ASSET_DIR}"/*.json "${ASSET_DIR}"/*.txt "${ASSET_DIR}"/*.status "${ASSET_DIR}"/*.log

log() {
  printf '[%s] %s\n' "$(date '+%H:%M:%S')" "$*" | tee -a "${RUN_LOG}"
}

pretty_json() {
  local path="$1"
  python3 - <<'PY' "${path}"
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
if not path.exists() or path.stat().st_size == 0:
    raise SystemExit(0)

data = json.loads(path.read_text())
path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")
PY
}

redact_top_level_key() {
  local path="$1"
  local key="$2"
  local replacement="$3"
  python3 - <<'PY' "${path}" "${key}" "${replacement}"
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
key = sys.argv[2]
replacement = sys.argv[3]

if not path.exists() or path.stat().st_size == 0:
    raise SystemExit(0)

data = json.loads(path.read_text())
if key in data:
    data[key] = replacement
path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")
PY
}

json_get() {
  local path="$1"
  local expr="$2"
  python3 - <<'PY' "${path}" "${expr}"
import json
import re
import sys

data = json.load(open(sys.argv[1]))
expr = sys.argv[2]
cur = data
for part in expr.split('.'):
    match = re.fullmatch(r'([A-Za-z0-9_:-]+)(?:\[(\d+)\])?', part)
    if not match:
        raise SystemExit(f"unsupported path expression: {expr}")
    key, index = match.group(1), match.group(2)
    cur = cur[key]
    if index is not None:
        cur = cur[int(index)]
print(cur)
PY
}

save_json_response() {
  local expected_status="$1"
  local method="$2"
  local url="$3"
  local output_path="$4"
  local bearer="$5"
  local payload="$6"
  shift 6 || true

  local temp_output
  local status
  local curl_args=(
    -sS
    -o "${output_path}.tmp"
    -w '%{http_code}'
    -X "${method}"
    "${url}"
  )

  if [[ -n "${payload}" ]]; then
    curl_args+=(-H 'Content-Type: application/json' --data "${payload}")
  fi
  if [[ -n "${bearer}" ]]; then
    curl_args+=(-H "Authorization: Bearer ${bearer}")
  fi
  while [[ $# -gt 0 ]]; do
    curl_args+=("$1")
    shift
  done

  status="$(curl "${curl_args[@]}")"
  if [[ "${status}" != "${expected_status}" ]]; then
    log "unexpected status ${status} for ${method} ${url}"
    if [[ -f "${output_path}.tmp" ]]; then
      cat "${output_path}.tmp" >&2
    fi
    rm -f "${output_path}.tmp"
    exit 1
  fi

  mv "${output_path}.tmp" "${output_path}"
  pretty_json "${output_path}"
  log "${method} ${url} -> ${status} saved to $(basename "${output_path}")"
}

save_text_response() {
  local expected_status="$1"
  local method="$2"
  local url="$3"
  local output_path="$4"
  local bearer="$5"
  local payload="$6"
  shift 6 || true

  local status
  local curl_args=(
    -sS
    -o "${output_path}.tmp"
    -w '%{http_code}'
    -X "${method}"
    "${url}"
  )

  if [[ -n "${payload}" ]]; then
    curl_args+=(-H 'Content-Type: application/json' --data "${payload}")
  fi
  if [[ -n "${bearer}" ]]; then
    curl_args+=(-H "Authorization: Bearer ${bearer}")
  fi
  while [[ $# -gt 0 ]]; do
    curl_args+=("$1")
    shift
  done

  status="$(curl "${curl_args[@]}")"
  if [[ "${status}" != "${expected_status}" ]]; then
    log "unexpected status ${status} for ${method} ${url}"
    if [[ -f "${output_path}.tmp" ]]; then
      cat "${output_path}.tmp" >&2
    fi
    rm -f "${output_path}.tmp"
    exit 1
  fi

  mv "${output_path}.tmp" "${output_path}"
  log "${method} ${url} -> ${status} saved to $(basename "${output_path}")"
}

cleanup() {
  if [[ -n "${API_PID:-}" ]]; then
    kill "${API_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${WORKER_PID:-}" ]]; then
    kill "${WORKER_PID}" >/dev/null 2>&1 || true
  fi
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
curl -sf "${BASE_URL}/readyz" >"${ASSET_DIR}/99-readyz.txt"

SUFFIX="$(python3 - <<'PY'
import time
print(int(time.time() * 1000))
PY
)"

OWNER_EMAIL="owner-${SUFFIX}@example.com"
SECOND_OWNER_EMAIL="owner2-${SUFFIX}@example.com"
MEMBER_EMAIL="member-${SUFFIX}@example.com"
OWNER_PASSWORD="OwnerPass123!"
MEMBER_PASSWORD="MemberPass123!"
ORG_SLUG="workspace-${SUFFIX}"
PROJECT_KEY="OPS${SUFFIX: -4}"

log "starting presentation demo scenario for organization ${ORG_SLUG}"

save_json_response "201" "POST" "${BASE_URL}/v1/auth/register-owner" "${ASSET_DIR}/01-register-owner.json" "" \
  "{\"email\":\"${OWNER_EMAIL}\",\"password\":\"${OWNER_PASSWORD}\",\"display_name\":\"Owner ${SUFFIX}\",\"org_name\":\"Workspace ${SUFFIX}\",\"org_slug\":\"${ORG_SLUG}\"}"
OWNER_ACCESS="$(json_get "${ASSET_DIR}/01-register-owner.json" "access_token")"
OWNER_REFRESH="$(json_get "${ASSET_DIR}/01-register-owner.json" "refresh_token")"
ORG_ID="$(json_get "${ASSET_DIR}/01-register-owner.json" "memberships[0].organization_id")"

save_json_response "201" "POST" "${BASE_URL}/v1/orgs/${ORG_ID}/projects" "${ASSET_DIR}/02-create-project.json" "${OWNER_ACCESS}" \
  "{\"name\":\"Operations\",\"project_key\":\"${PROJECT_KEY}\"}"
PROJECT_ID="$(json_get "${ASSET_DIR}/02-create-project.json" "project.id")"

save_json_response "201" "POST" "${BASE_URL}/v1/orgs/${ORG_ID}/invitations" "${ASSET_DIR}/03-create-invitation.json" "${OWNER_ACCESS}" \
  "{\"email\":\"${MEMBER_EMAIL}\",\"role\":\"member\"}" \
  -H 'Idempotency-Key: invite-demo-1'
INVITE_TOKEN="$(json_get "${ASSET_DIR}/03-create-invitation.json" "accept_token_preview")"

save_json_response "200" "POST" "${BASE_URL}/v1/invitations/accept" "${ASSET_DIR}/04-accept-invitation.json" "" \
  "{\"token\":\"${INVITE_TOKEN}\",\"display_name\":\"Member ${SUFFIX}\",\"password\":\"${MEMBER_PASSWORD}\"}"
MEMBER_ACCESS="$(json_get "${ASSET_DIR}/04-accept-invitation.json" "access_token")"
MEMBER_ID="$(json_get "${ASSET_DIR}/04-accept-invitation.json" "user.id")"

save_json_response "201" "POST" "${BASE_URL}/v1/projects/${PROJECT_ID}/issues" "${ASSET_DIR}/05-create-issue.json" "${MEMBER_ACCESS}" \
  "{\"title\":\"Investigate dashboard lag\",\"description\":\"Summary endpoint needs profiling\"}" \
  -H 'Idempotency-Key: issue-demo-1'
ISSUE_ID="$(json_get "${ASSET_DIR}/05-create-issue.json" "issue.id")"
ISSUE_VERSION="$(json_get "${ASSET_DIR}/05-create-issue.json" "issue.version")"

save_json_response "200" "POST" "${BASE_URL}/v1/projects/${PROJECT_ID}/issues" "${ASSET_DIR}/06-replay-issue.json" "${MEMBER_ACCESS}" \
  "{\"title\":\"Investigate dashboard lag\",\"description\":\"Summary endpoint needs profiling\"}" \
  -H 'Idempotency-Key: issue-demo-1'

save_json_response "409" "PATCH" "${BASE_URL}/v1/issues/${ISSUE_ID}" "${ASSET_DIR}/07-update-conflict.json" "${OWNER_ACCESS}" \
  "{\"status\":\"done\",\"assignee_user_id\":\"${MEMBER_ID}\",\"version\":999}"

save_json_response "200" "PATCH" "${BASE_URL}/v1/issues/${ISSUE_ID}" "${ASSET_DIR}/08-update-issue.json" "${OWNER_ACCESS}" \
  "{\"status\":\"in_progress\",\"assignee_user_id\":\"${MEMBER_ID}\",\"version\":${ISSUE_VERSION}}"

save_json_response "201" "POST" "${BASE_URL}/v1/issues/${ISSUE_ID}/comments" "${ASSET_DIR}/09-add-comment.json" "${MEMBER_ACCESS}" \
  '{"body":"Initial triage complete. Profiling next."}'

sleep 1

save_json_response "200" "GET" "${BASE_URL}/v1/orgs/${ORG_ID}/notifications" "${ASSET_DIR}/10-notifications.json" "${OWNER_ACCESS}" ""
save_json_response "200" "GET" "${BASE_URL}/v1/orgs/${ORG_ID}/dashboard/summary" "${ASSET_DIR}/11-dashboard-summary.json" "${OWNER_ACCESS}" ""

save_json_response "200" "POST" "${BASE_URL}/v1/auth/refresh" "${ASSET_DIR}/12-refresh.json" "" \
  "{\"refresh_token\":\"${OWNER_REFRESH}\"}"
NEW_REFRESH="$(json_get "${ASSET_DIR}/12-refresh.json" "refresh_token")"

save_text_response "204" "POST" "${BASE_URL}/v1/auth/logout" "${ASSET_DIR}/13-logout.status" "" \
  "{\"refresh_token\":\"${NEW_REFRESH}\"}"

save_json_response "401" "POST" "${BASE_URL}/v1/auth/refresh" "${ASSET_DIR}/14-refresh-after-logout.json" "" \
  "{\"refresh_token\":\"${NEW_REFRESH}\"}"

save_json_response "201" "POST" "${BASE_URL}/v1/auth/register-owner" "${ASSET_DIR}/15-register-second-owner.json" "" \
  "{\"email\":\"${SECOND_OWNER_EMAIL}\",\"password\":\"${OWNER_PASSWORD}\",\"display_name\":\"Owner Two ${SUFFIX}\",\"org_name\":\"Workspace Two ${SUFFIX}\",\"org_slug\":\"workspace-two-${SUFFIX}\"}"
SECOND_OWNER_ACCESS="$(json_get "${ASSET_DIR}/15-register-second-owner.json" "access_token")"

save_json_response "403" "GET" "${BASE_URL}/v1/orgs/${ORG_ID}/projects" "${ASSET_DIR}/16-cross-tenant-forbidden.json" "${SECOND_OWNER_ACCESS}" ""

curl -sS "${BASE_URL}/metrics" >"${ASSET_DIR}/17-metrics.txt"

redact_top_level_key "${ASSET_DIR}/01-register-owner.json" "access_token" "<redacted-demo-access-token>"
redact_top_level_key "${ASSET_DIR}/01-register-owner.json" "refresh_token" "<redacted-demo-refresh-token>"
redact_top_level_key "${ASSET_DIR}/03-create-invitation.json" "accept_token_preview" "<redacted-demo-invite-token>"
redact_top_level_key "${ASSET_DIR}/04-accept-invitation.json" "access_token" "<redacted-demo-access-token>"
redact_top_level_key "${ASSET_DIR}/04-accept-invitation.json" "refresh_token" "<redacted-demo-refresh-token>"
redact_top_level_key "${ASSET_DIR}/12-refresh.json" "access_token" "<redacted-demo-access-token>"
redact_top_level_key "${ASSET_DIR}/12-refresh.json" "refresh_token" "<redacted-demo-refresh-token>"
redact_top_level_key "${ASSET_DIR}/15-register-second-owner.json" "access_token" "<redacted-demo-access-token>"
redact_top_level_key "${ASSET_DIR}/15-register-second-owner.json" "refresh_token" "<redacted-demo-refresh-token>"

log "presentation demo capture complete"

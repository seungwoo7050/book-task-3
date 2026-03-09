#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${ROOT_DIR}/docker-compose.postgres.yml"
QUALBOT_POSTGRES_PORT="${QUALBOT_POSTGRES_PORT:-55432}"
: "${UV_PYTHON:=python3.12}"

compose() {
  docker compose -f "${COMPOSE_FILE}" "$@"
}

cleanup() {
  compose down -v >/dev/null 2>&1 || true
}

trap cleanup EXIT

compose up -d >/dev/null
POSTGRES_CONTAINER_ID="$(compose ps -q postgres)"

for _ in $(seq 1 30); do
  status="$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "${POSTGRES_CONTAINER_ID}")"
  if [[ "${status}" == "healthy" ]]; then
    break
  fi
  sleep 1
done

status="$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "${POSTGRES_CONTAINER_ID}")"
if [[ "${status}" != "healthy" ]]; then
  echo "PostgreSQL container did not become healthy" >&2
  compose ps >&2
  exit 1
fi

QUALBOT_DB_URL="postgresql+psycopg://qualbot:qualbot@127.0.0.1:${QUALBOT_POSTGRES_PORT}/qualbot" \
PYTHONPATH=backend/src \
UV_PYTHON="${UV_PYTHON}" \
uv run python - <<'PY'
from datetime import UTC, datetime

from sqlalchemy import select, text

from db.database import init_db, reset_engines, session_scope
from db.models import Conversation

reset_engines()
init_db()

with session_scope() as session:
    probe = session.execute(text("select 1")).scalar_one()
    assert probe == 1
    session.merge(
        Conversation(
            id="postgres-smoke-conversation",
            prompt_version="v1.0",
            kb_version="v1.0",
            created_at=datetime.now(UTC),
        )
    )

with session_scope() as session:
    conversation_id = session.scalar(
        select(Conversation.id).where(Conversation.id == "postgres-smoke-conversation")
    )
    if conversation_id != "postgres-smoke-conversation":
        raise SystemExit("PostgreSQL smoke verification failed")

print("PostgreSQL smoke verification passed")
PY

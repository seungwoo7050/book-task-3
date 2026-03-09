#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 <workspace-fastapi-dir> <host-port>" >&2
  exit 1
fi

workspace="$1"
port="$2"
project_name="$(printf '%s' "${workspace}" | tr '[:upper:]/._' '[:lower:]---' | tr -cd '[:lower:][:digit:]-_')"
created_env=0

cleanup() {
  docker compose -p "${project_name}" -f "${workspace}/compose.yaml" down -v --remove-orphans >/dev/null 2>&1 || true
  if [ "${created_env}" -eq 1 ]; then
    rm -f "${workspace}/.env"
  fi
}

wait_for_health() {
  local path="$1"
  local url="http://127.0.0.1:${port}${path}"

  for _ in $(seq 1 60); do
    if curl -fsS "${url}" >/dev/null; then
      echo "healthy: ${url}"
      return 0
    fi
    sleep 2
  done

  echo "health probe failed: ${url}" >&2
  docker compose -p "${project_name}" -f "${workspace}/compose.yaml" ps >&2 || true
  docker compose -p "${project_name}" -f "${workspace}/compose.yaml" logs >&2 || true
  return 1
}

trap cleanup EXIT

if [ ! -f "${workspace}/.env" ]; then
  cp "${workspace}/.env.example" "${workspace}/.env"
  created_env=1
fi

docker compose -p "${project_name}" -f "${workspace}/compose.yaml" up --build -d
wait_for_health "/api/v1/health/live"
wait_for_health "/api/v1/health/ready"

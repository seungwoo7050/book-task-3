#!/usr/bin/env bash
set -euo pipefail

BUILD_DIR="${1:-../cpp/build}"
TCP_PORT=39101
UDP_PORT=39102
DB_PATH="$(pwd)/data/demo.sqlite3"

rm -f "${DB_PATH}"

"${BUILD_DIR}/arena_server" \
  --tcp-port "${TCP_PORT}" \
  --udp-port "${UDP_PORT}" \
  --db-path "${DB_PATH}" \
  --thread-count 2 \
  --match-duration-ms 5000 \
  --resume-window-ms 1000 >/tmp/tactical_arena_demo_server.log 2>&1 &
SERVER_PID=$!
trap 'kill ${SERVER_PID} >/dev/null 2>&1 || true; wait ${SERVER_PID} >/dev/null 2>&1 || true' EXIT INT TERM

sleep 1

"${BUILD_DIR}/arena_bot" \
  --host 127.0.0.1 \
  --tcp-port "${TCP_PORT}" \
  --mode scripted \
  --role host \
  --name demo-alpha \
  --room-name demo \
  --max-players 2 &
BOT_A_PID=$!

sleep 0.2

"${BUILD_DIR}/arena_bot" \
  --host 127.0.0.1 \
  --tcp-port "${TCP_PORT}" \
  --mode scripted \
  --role join \
  --name demo-beta \
  --room-name demo &
BOT_B_PID=$!

wait "${BOT_A_PID}"
wait "${BOT_B_PID}"

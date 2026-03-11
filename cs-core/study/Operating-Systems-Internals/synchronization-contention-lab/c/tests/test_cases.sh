#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$ROOT_DIR/bin/contention_lab"

extract() {
  local key="$1"
  awk -F= -v k="$key" '$1 == k { print $2 }'
}

counter_output="$("$BIN" --scenario counter --threads 8 --iterations 10000)"
echo "$counter_output" | grep '^ok=1$' >/dev/null
counter_final="$(echo "$counter_output" | extract final_count)"
counter_expected="$(echo "$counter_output" | extract expected_count)"
[[ "$counter_final" == "$counter_expected" ]]

gate_output="$("$BIN" --scenario gate --threads 8 --iterations 5000)"
echo "$gate_output" | grep '^ok=1$' >/dev/null
gate_max="$(echo "$gate_output" | extract max_concurrency)"
gate_limit="$(echo "$gate_output" | extract permit_limit)"
[[ "$gate_max" -le "$gate_limit" ]]

buffer_output="$("$BIN" --scenario buffer --threads 8 --iterations 4000)"
echo "$buffer_output" | grep '^ok=1$' >/dev/null
produced="$(echo "$buffer_output" | extract produced)"
consumed="$(echo "$buffer_output" | extract consumed)"
underflow="$(echo "$buffer_output" | extract underflow)"
overflow="$(echo "$buffer_output" | extract overflow)"
[[ "$produced" == "$consumed" ]]
[[ "$underflow" == "0" ]]
[[ "$overflow" == "0" ]]

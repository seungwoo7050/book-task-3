#!/usr/bin/env bash

set -euo pipefail

PROXY_BIN=${1:?usage: run_proxy_tests.sh <proxy-binary>}
TEST_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_DIR="$(mktemp -d)"
ORIGIN_PID=""
PROXY_PID=""

pick_port() {
    python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
}

cleanup() {
    if [[ -n "$PROXY_PID" ]]; then
        kill "$PROXY_PID" 2>/dev/null || true
        wait "$PROXY_PID" 2>/dev/null || true
    fi
    if [[ -n "$ORIGIN_PID" ]]; then
        kill "$ORIGIN_PID" 2>/dev/null || true
        wait "$ORIGIN_PID" 2>/dev/null || true
    fi
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

ORIGIN_PORT="$(pick_port)"
PROXY_PORT="$(pick_port)"

chmod +x "$TEST_DIR/origin_server.py"
python3 "$TEST_DIR/origin_server.py" "$ORIGIN_PORT" > "$TMP_DIR/origin.log" 2>&1 &
ORIGIN_PID=$!

for _ in $(seq 1 20); do
    if curl -sS --max-time 2 "http://127.0.0.1:$ORIGIN_PORT/health" >/dev/null 2>&1; then
        break
    fi
    sleep 0.2
done

"$PROXY_BIN" "$PROXY_PORT" > "$TMP_DIR/proxy.log" 2>&1 &
PROXY_PID=$!
sleep 1

body="$(curl --noproxy '' -sS --max-time 5 -x "http://127.0.0.1:$PROXY_PORT" "http://127.0.0.1:$ORIGIN_PORT/cacheable/basic")"
grep -q "cacheable path=/cacheable/basic hit=1" <<<"$body"

header_body="$(curl --noproxy '' -sS --max-time 5 -x "http://127.0.0.1:$PROXY_PORT" \
    -H "User-Agent: BadAgent" \
    -H "Connection: keep-alive" \
    -H "Proxy-Connection: keep-alive" \
    -H "X-Test: forwarded" \
    "http://127.0.0.1:$ORIGIN_PORT/headers")"
grep -q "host=127.0.0.1:$ORIGIN_PORT" <<<"$header_body"
grep -q "user-agent=Mozilla/5.0" <<<"$header_body"
grep -q "connection=close" <<<"$header_body"
grep -q "proxy-connection=close" <<<"$header_body"
grep -q "x-test=forwarded" <<<"$header_body"

first_cache="$(curl --noproxy '' -sS --max-time 5 -x "http://127.0.0.1:$PROXY_PORT" "http://127.0.0.1:$ORIGIN_PORT/cacheable/reuse")"
second_cache="$(curl --noproxy '' -sS --max-time 5 -x "http://127.0.0.1:$PROXY_PORT" "http://127.0.0.1:$ORIGIN_PORT/cacheable/reuse")"
grep -q "hit=1" <<<"$first_cache"
grep -q "hit=1" <<<"$second_cache"

first_large_file="$TMP_DIR/large1.out"
second_large_file="$TMP_DIR/large2.out"
curl --noproxy '' -sS --max-time 10 -x "http://127.0.0.1:$PROXY_PORT" "http://127.0.0.1:$ORIGIN_PORT/large/object" -o "$first_large_file"
curl --noproxy '' -sS --max-time 10 -x "http://127.0.0.1:$PROXY_PORT" "http://127.0.0.1:$ORIGIN_PORT/large/object" -o "$second_large_file"
grep -a -q "hit=1" "$first_large_file"
grep -a -q "hit=2" "$second_large_file"

elapsed="$(ORIGIN_PORT="$ORIGIN_PORT" PROXY_PORT="$PROXY_PORT" python3 - <<'PY'
import os
import subprocess
import time

origin = os.environ["ORIGIN_PORT"]
proxy = os.environ["PROXY_PORT"]

def launch(path: str):
    return subprocess.Popen(
        [
            "curl",
            "--noproxy", "",
            "-sS",
            "--max-time", "8",
            "-x", f"http://127.0.0.1:{proxy}",
            f"http://127.0.0.1:{origin}{path}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

start = time.time()
p1 = launch("/slow/one")
p2 = launch("/slow/two")
o1, e1 = p1.communicate()
o2, e2 = p2.communicate()
elapsed = time.time() - start

if p1.returncode != 0 or p2.returncode != 0:
    raise SystemExit("curl failed")
if "slow path=/slow/one" not in o1 or "slow path=/slow/two" not in o2:
    raise SystemExit("unexpected response body")

print(f"{elapsed:.3f}")
PY
)"

ELAPSED="$elapsed" python3 - <<'PY'
import os
elapsed = float(os.environ["ELAPSED"])
if elapsed >= 3.5:
    raise SystemExit(f"concurrency check failed: elapsed={elapsed:.3f}")
PY

curl --noproxy '' -sS --max-time 3 -o /dev/null -x "http://127.0.0.1:$PROXY_PORT" "http://127.0.0.1:1/" || true
body="$(curl --noproxy '' -sS --max-time 5 -x "http://127.0.0.1:$PROXY_PORT" "http://127.0.0.1:$ORIGIN_PORT/cacheable/post-failure")"
grep -q "cacheable path=/cacheable/post-failure hit=1" <<<"$body"

echo "Proxy tests passed"

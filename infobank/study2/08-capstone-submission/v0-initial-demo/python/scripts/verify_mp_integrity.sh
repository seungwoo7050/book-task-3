#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-all}"
: "${UV_PYTHON:=python3.12}"

run_uv() {
  UV_PYTHON="${UV_PYTHON}" PYTHONPATH=backend/src uv run "$@"
}

step() {
  printf "\n==> %s\n" "$1"
}

run_lint() {
  step "Lint (ruff)"
  run_uv ruff check backend/src tests
}

run_typecheck() {
  step "Type check (mypy)"
  run_uv mypy backend/src
}

run_mp1() {
  step "MP1 tests"
  run_uv pytest -q tests/mp1
}

run_mp2() {
  step "MP2 tests"
  run_uv pytest -q tests/mp2
}

run_mp3() {
  step "MP3 tests"
  run_uv pytest -q tests/mp3
}

run_mp4() {
  step "MP4 tests"
  run_uv pytest -q tests/mp4
}

run_mp5() {
  step "MP5 tests"
  run_uv pytest -q tests/mp5
}

run_frontend() {
  step "Frontend tests"
  (
    cd ../react
    if [[ -f pnpm-lock.yaml ]]; then
      pnpm install --frozen-lockfile
    else
      pnpm install
    fi
    pnpm test --run
  )
}

gate_mp1() {
  run_mp1
}

gate_mp2() {
  run_mp1
  run_mp2
}

gate_mp3() {
  run_mp1
  run_mp2
  run_mp3
}

gate_mp4() {
  run_mp1
  run_mp2
  run_mp3
  run_mp4
}

gate_mp5() {
  run_mp1
  run_mp2
  run_mp3
  run_mp4
  run_mp5
}

case "$TARGET" in
  mp1)
    run_lint
    run_typecheck
    gate_mp1
    ;;
  mp2)
    run_lint
    run_typecheck
    gate_mp2
    ;;
  mp3)
    run_lint
    run_typecheck
    gate_mp3
    ;;
  mp4)
    run_lint
    run_typecheck
    gate_mp4
    ;;
  mp5)
    run_lint
    run_typecheck
    gate_mp5
    ;;
  all)
    run_lint
    run_typecheck
    gate_mp5
    run_frontend
    ;;
  *)
    echo "Usage: $0 [mp1|mp2|mp3|mp4|mp5|all]"
    exit 2
    ;;
esac

step "Integrity gate passed for target=${TARGET}"

# v1 회귀 안정화

`v1-regression-hardening`은 `v0-initial-demo`를 바탕으로 회귀 검증, provider fallback, lineage 노출, PostgreSQL smoke path를 강화한 버전이다. "데모가 한 번 돌아간다"를 넘어서 "개선 여부를 비교하고 운영 경로를 점검할 수 있다"까지 끌어올리는 것이 목표다.

## 이번 버전에서 달라진 점

- golden set 커버리지 확대
- run-level 회귀 검증과 version compare 강화
- Upstage Solar -> OpenAI -> Ollama provider chain 추가
- dependency health와 fallback 경로 안정화
- Langfuse lineage/trace envelope 준비
- PostgreSQL smoke path와 SQLite fallback 정리

## 검증 명령

- `cd python && UV_PYTHON=python3.12 make gate-all`
- `cd python && UV_PYTHON=python3.12 make smoke-postgres`

## 먼저 볼 문서

- [`problem/README.md`](./problem/README.md)
- [`docs/README.md`](./docs/README.md)
- [`docs/demo/demo-runbook.md`](./docs/demo/demo-runbook.md)
- [`docs/presentation/v1-demo-presentation.md`](./docs/presentation/v1-demo-presentation.md)

## 현재 상태

- `v0`의 runnable baseline을 유지하면서 trace 노출과 운영 검증을 실제 구현 수준까지 끌어올린 상태다.
- 학생 입장에서는 "기능 추가"보다 "회귀 안정화와 비교 가능성"을 어떻게 문서화하는지 참고하기 좋은 버전이다.

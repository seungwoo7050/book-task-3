# v0 초기 데모

`v0-initial-demo`는 Chat QA Ops 트랙에서 처음 끝까지 실행해 볼 수 있는 baseline snapshot이다. rubric, guardrail, evidence verifier, judge/score merge, golden replay, 운영 대시보드를 한 번에 연결해 "품질 관리 시스템이 실제로 어떻게 보이는지"를 보여 주는 것이 목표다.

## 이 버전에서 확인할 것

- `python/`에서 FastAPI API, CLI, evaluator pipeline, seeded KB, replay harness를 함께 확인할 수 있다.
- `react/`에서는 overview, failures, session review, eval runner 화면을 바로 실행해 볼 수 있다.
- `docs/demo/`에는 시연 runbook, proof artifact, 시나리오 문서가 정리돼 있다.
- `SQLite + heuristic` 중심의 빠른 재현 경로가 기본값이고, 더 무거운 운영 경로는 이후 버전에서 확장한다.

## 실행 순서

```bash
cd python
uv sync --extra dev
make init-db
make seed-demo
make test-backend
make run-backend
```

별도 터미널에서:

```bash
cd react
pnpm install
pnpm test --run
pnpm dev
```

## 현재 범위

- 상담 품질 기준 정의
- 규칙/가드레일과 근거 검증
- judge scoring과 golden set replay
- overview, failures, session review, eval runner UI
- replay fixture와 proof artifact 재생성 경로
- escalation warning, dependency health, fallback contract 테스트

## 먼저 볼 문서

- [`problem/README.md`](./problem/README.md)
- [`docs/README.md`](./docs/README.md)
- [`docs/demo/demo-runbook.md`](./docs/demo/demo-runbook.md)
- [`docs/presentation/v0-demo-presentation.md`](./docs/presentation/v0-demo-presentation.md)

## 현재 상태

- 빠른 재현성을 위해 `SQLite`와 로컬 fallback 중심으로 유지한다.
- `PostgreSQL`, `Langfuse`, `Upstage Solar/OpenAI/Ollama` adapter chain은 이후 버전에서 단계적으로 반영한다.
- proof artifact 기본 출력 위치는 [`docs/demo/proof-artifacts`](./docs/demo/proof-artifacts/)다.

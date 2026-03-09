# Study 2 Capstone v0

`v0-initial-demo`는 최초 제출 가능한 Chat QA Ops 데모다.
현재 목표는 품질 평가 파이프라인과 운영 UI를 끝까지 한 번 연결해 보여주는 것이다.

## Included

- `python/`: FastAPI, CLI, evaluator pipeline, tests
- `react/`: 운영 대시보드 UI
- `docs/demo/`: 시연 시나리오와 proof 문서

## Run

### Backend

```bash
cd python
uv sync --extra dev
make init-db
make seed-demo
make test-backend
```

### Frontend

```bash
cd react
pnpm install
pnpm test --run
```

### End-to-end demo

```bash
cd python
make run-backend
```

별도 터미널에서:

```bash
cd react
pnpm dev
```

## Scope

- 상담 품질 기준 정의
- 규칙/가드레일 + 근거 검증 + judge scoring
- golden set replay
- overview, failures, session review, eval runner UI
- replay fixture와 proof artifact 재생성 경로 정리
- escalation warning, dependency health, fallback contract 테스트 포함

## Current Implementation Note

- 현재 runnable snapshot은 빠른 재현성을 위해 `SQLite`와 로컬 fallback 중심으로 유지한다.
- 최종 설계 기준의 `PostgreSQL`, `Langfuse`, `Upstage Solar/OpenAI/Ollama` adapter chain은 이후 버전에서 단계적으로 반영한다.
- proof artifact 기본 출력 위치는 [`docs/demo/proof-artifacts`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v0-initial-demo/docs/demo/proof-artifacts)다.
- 발표용 문서는 [`docs/presentation/v0-demo-presentation.md`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v0-initial-demo/docs/presentation/v0-demo-presentation.md)에 정리했다.

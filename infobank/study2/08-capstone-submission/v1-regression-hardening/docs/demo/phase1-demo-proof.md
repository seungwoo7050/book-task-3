# Phase1 Demo Proof (Executable Evidence)

## Run timestamp
- KST: 2026-03-05 23:07:01
- Source: `docs/demo/proof-artifacts/run-timestamp.txt`

## Environment
- Backend: FastAPI (`uvicorn api.main:app`) on `127.0.0.1:8000`
- Frontend: React/Vite on `127.0.0.1:5173`
- DB: SQLite (`backend/data/qualbot.db`)
- 증빙 재수집 기본 모드: `QUALBOT_EVAL_MODE=llm` (strict)
- 비상 모드: `QUALBOT_EVAL_MODE=heuristic` (운영자 명시 전환 시에만 허용)

## Step 1) Preflight + 증빙 재수집
```bash
make preflight
QUALBOT_OLLAMA_JUDGE_MODEL=qwen2.5:3b \
QUALBOT_OLLAMA_CLAIM_MODEL=qwen2.5:3b \
QUALBOT_OLLAMA_EVIDENCE_MODEL=qwen2.5:3b \
qualbot demo-proof --mode llm --limit 5
```

Result artifacts:
- `docs/demo/proof-artifacts/api-dependency-health.json`
- `docs/demo/proof-artifacts/api-golden-run.json`
- `docs/demo/proof-artifacts/api-overview.json`
- `docs/demo/proof-artifacts/api-failures.json`
- `docs/demo/proof-artifacts/api-pipeline-stats.json`
- `docs/demo/proof-artifacts/cli-evaluate-golden.txt`
- `docs/demo/proof-artifacts/cli-report.txt`

Expected output excerpt (`cli-evaluate-golden.txt`):
```text
evaluated=5 avg_score=65.48 critical=0 pass_count=1 fail_count=4
```

## Step 2) strict 계약 확인 포인트
1. `api-dependency-health.json`
- `eval_mode=llm`
- `policy=strict`
- `models_configured=true`

2. `api-golden-run.json`
- `pass_count`, `fail_count`, `assertion_failures` 필드 존재
- `pass_count + fail_count == count`
 - latest: `count=5`, `pass_count=1`, `fail_count=4`

3. `api-pipeline-stats.json`
- `retrieval_backend=chroma`
- `judge_model`/`claim_model`/`evidence_model`이 heuristic 이름이 아님
- `dependency_fail_count` 확인 가능
 - latest: `judge/claim/evidence=qwen2.5:3b`, `dependency_fail_count=0`

## Step 3-1) dependency failure contract check
```bash
GET /api/evaluate/turn/{id}  # Ollama/Chroma 비가동 상태
```

Result excerpt:
- `503`
- `{"error_code":"DEPENDENCY_UNAVAILABLE","component":"ollama|chroma","message":"..."}`

## Step 4) UI evidence screenshots
- Overview: `docs/demo/proof-artifacts/overview.png`
- Failures: `docs/demo/proof-artifacts/failures.png`
- Session Review: `docs/demo/proof-artifacts/sessions.png`
- Eval Runner: `docs/demo/proof-artifacts/runner.png`

## Verification conclusion
- Phase1 시연 플로우(배치평가 -> Overview -> Failures -> SessionReview -> Report) 실제 실행 가능.
- 데이터/점수/실패유형이 CLI와 API/대시보드에서 확인됨.

## Fixes applied during proof run
1. Frontend fetch 차단 이슈 해결: FastAPI CORS middleware 추가.
2. `qualbot report` 예외 해결: SQLAlchemy session `expire_on_commit=False` 적용.
3. Session Review score 표시 누락 해결: 평가 저장 flush 후 conversation score 집계.

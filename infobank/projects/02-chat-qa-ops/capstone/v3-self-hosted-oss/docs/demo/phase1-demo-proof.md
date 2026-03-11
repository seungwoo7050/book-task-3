# Phase1 데모 증빙 (실행 증거)

## 실행 시각
- KST: 2026-03-05 23:07:01
- Source: `docs/demo/proof-artifacts/run-timestamp.txt`

## 환경
- Backend: FastAPI (`uvicorn api.main:app`) on `127.0.0.1:8000`
- Frontend: React/Vite on `127.0.0.1:5173`
- DB: SQLite (`backend/data/qualbot.db`)
- 증빙 재수집 기본 모드: `QUALBOT_EVAL_MODE=llm` (strict)
- 비상 모드: `QUALBOT_EVAL_MODE=heuristic` (운영자 명시 전환 시에만 허용)

## 1단계) 사전 점검 + 증빙 재수집
```bash
make preflight
QUALBOT_OLLAMA_JUDGE_MODEL=qwen2.5:3b \
QUALBOT_OLLAMA_CLAIM_MODEL=qwen2.5:3b \
QUALBOT_OLLAMA_EVIDENCE_MODEL=qwen2.5:3b \
qualbot demo-proof --mode llm --limit 5
```

생성된 증빙 파일:
- `docs/demo/proof-artifacts/api-dependency-health.json`
- `docs/demo/proof-artifacts/api-golden-run.json`
- `docs/demo/proof-artifacts/api-overview.json`
- `docs/demo/proof-artifacts/api-failures.json`
- `docs/demo/proof-artifacts/api-pipeline-stats.json`
- `docs/demo/proof-artifacts/cli-evaluate-golden.txt`
- `docs/demo/proof-artifacts/cli-report.txt`

기대 출력 발췌 (`cli-evaluate-golden.txt`):
```text
evaluated=5 avg_score=65.48 critical=0 pass_count=1 fail_count=4
```

## 2단계) strict 계약 확인 포인트
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

## 3-1단계) 의존성 장애 계약 확인
```bash
GET /api/evaluate/turn/{id}  # Ollama/Chroma 비가동 상태
```

결과 발췌:
- `503`
- `{"error_code":"DEPENDENCY_UNAVAILABLE","component":"ollama|chroma","message":"..."}`

## 4단계) UI 증빙 스크린샷
- Overview: `docs/demo/proof-artifacts/overview.png`
- Failures: `docs/demo/proof-artifacts/failures.png`
- Session Review: `docs/demo/proof-artifacts/sessions.png`
- Eval Runner: `docs/demo/proof-artifacts/runner.png`

## 검증 결론
- Phase1 시연 플로우(배치평가 -> Overview -> Failures -> SessionReview -> Report) 실제 실행 가능.
- 데이터/점수/실패유형이 CLI와 API/대시보드에서 확인됨.

## 증빙 실행 중 적용한 수정
1. Frontend fetch 차단 이슈 해결: FastAPI CORS middleware 추가.
2. `qualbot report` 예외 해결: SQLAlchemy session `expire_on_commit=False` 적용.
3. Session Review score 표시 누락 해결: 평가 저장 flush 후 conversation score 집계.

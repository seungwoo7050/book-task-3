# Chat QA Ops v2

챗봇 상담 품질 관리 시스템의 Phase 1(필수) 완성과 Phase 2(가산점 훅) 선반영을 목표로 하는 프로젝트다.

## 핵심 목표

- 상담 품질 기준 정의 및 점수화
- 자동 평가 파이프라인 (Rule -> Evidence -> LLM Judge -> Scoring)
- 운영 대시보드 가시화 (Overview/Failures/Session Review/Eval Runner)
- Phase 2 비교 훅 (`version_compare`, `pipeline_stats`) 선반영

## 디렉터리

```text
chat-bot/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   ├── chatbot/
│   │   ├── evaluator/
│   │   ├── cli/
│   │   ├── db/
│   │   └── core/
│   ├── knowledge_base/
│   ├── rules/
│   ├── prompts/
│   └── golden_set/
├── frontend/
├── tests/
├── docs/demo/
├── pyproject.toml
└── Makefile
```

## 빠른 시작

### 1) Python 환경

```bash
cd chat-bot
make backend-install
make init-db
make seed-demo
```

### 2) 백엔드 실행

```bash
export QUALBOT_EVAL_MODE=llm
export QUALBOT_RETRIEVAL_BACKEND=chroma
export QUALBOT_ENABLE_OLLAMA=1
export QUALBOT_ENABLE_CHROMA=1
export QUALBOT_OLLAMA_JUDGE_MODEL=<judge-model>
export QUALBOT_OLLAMA_CLAIM_MODEL=<claim-model>
export QUALBOT_OLLAMA_EVIDENCE_MODEL=<evidence-model>
make run-backend
```

기본 URL: `http://localhost:8000`

### 3) CLI 사용

```bash
make chat MSG="프리미엄 요금제 해지 시 위약금이 있나요?"
make evaluate-golden
make report
make preflight
make demo-proof-llm
```

### 4) 프론트엔드 실행

```bash
make frontend-install
make run-frontend
```

기본 URL: `http://localhost:5173`

## MP 단계 게이트 (무결성 검증)

각 미니프로젝트는 선행 단계 테스트를 누적 통과해야 다음 단계로 진행한다.

```bash
make gate-mp1   # lint + mypy + mp1
make gate-mp2   # lint + mypy + mp1~mp2 누적
make gate-mp3   # lint + mypy + mp1~mp3 누적
make gate-mp4   # lint + mypy + mp1~mp4 누적
make gate-mp5   # lint + mypy + mp1~mp5 누적
make gate-all   # 전체 누적 + frontend 테스트
```

## 주요 API

- `POST /api/chat`
- `GET /api/conversations`
- `GET /api/conversations/{id}`
- `POST /api/evaluate/turn/{id}`
- `POST /api/evaluate/conversation/{id}`
- `POST /api/evaluate/batch`
- `GET /api/evaluations`
- `GET /api/evaluations/{id}`
- `GET /api/dashboard/overview`
- `GET /api/dashboard/failures`
- `GET /api/dashboard/metrics`
- `GET /api/dashboard/version-compare`
- `GET /api/system/pipeline-stats`
- `GET /api/system/dependency-health`
- `GET /api/golden-set`
- `POST /api/golden-set`
- `POST /api/golden-set/run`

`/api/golden-set/run` v1.5 추가 필드:
- `pass_count`
- `fail_count`
- `assertion_failures`

의존성 장애 시 평가 API 응답:
- HTTP `503`
- `{ "error_code": "DEPENDENCY_UNAVAILABLE", "message": "...", "component": "ollama|chroma|runtime" }`

## 신규 CLI (v1.6)

- `qualbot preflight`
  - 현재 env/모델/의존성(ollama/chroma) 상태를 점검하고, `llm` 모드면 strict 계약을 검증한다.
- `qualbot demo-proof --mode llm|heuristic`
  - `docs/demo/proof-artifacts` 아래 데모 증빙 JSON/TXT를 재생성한다.

## 데모 문서

- `docs/demo/phase1-demo-scenario.md`
- `docs/demo/phase1-e2e-user-scenarios-ko.md` (v1.5 시나리오/스크린샷 기준 문서)
- `docs/demo/phase2-demo-scenario.md`
- `docs/demo/phase1-vs-phase2-diff-matrix.md`
- `docs/demo/demo-runbook.md`
- `docs/demo/demo-fallbacks.md`
- `docs/demo/phase1-demo-proof.md`

## 모노레포 로컬 스냅샷 (v1 고정)

상위 종합 레포에 다른 프로젝트 변경이 섞여 있을 때는 커밋 분리 대신 폴더 스냅샷으로 고정한다.

```bash
cd chat-bot
chmod +x scripts/snapshot_chatbot.sh

# v1 고정 스냅샷 생성 (읽기 전용)
./scripts/snapshot_chatbot.sh create v1.0-freeze

# 스냅샷 목록
./scripts/snapshot_chatbot.sh list

# 특정 스냅샷에서 복원본 생성
./scripts/snapshot_chatbot.sh restore <snapshot-folder-name>
```

기본 스냅샷 저장 위치:
- `../_snapshots/chat-bot`

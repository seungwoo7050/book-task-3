# Chat QA Ops 공개 정리 기준

이 문서는 `chat-qa-ops/` 트랙을 공개 레포 기준으로 어떻게 읽고 검증하면 되는지 한 장으로 요약한다.

## 공개 범위

- 주제: 한국어 챗봇 상담 품질 관리
- 목표: rule/guardrail, evidence verification, judge scoring, golden regression, monitoring UI를 단계적으로 학습하고 최종적으로 QA Ops capstone demo로 묶는다.
- 포함 대상: README, stage implementation pack, capstone snapshot, proof artifact, `notion/` 백업 문서

## 무엇이 들어 있는가

- `00~07`: capstone 개념을 분리해 학습할 수 있는 stage pack
- `08-capstone-submission/v0`: runnable baseline snapshot
- `08-capstone-submission/v1`: regression hardening, provider chain, lineage/trace, PostgreSQL smoke path
- `08-capstone-submission/v2`: retrieval improvement experiment와 compare proof
- `08-capstone-submission/v3`: self-hosted OSS snapshot

## 문서와 노트 운영 규칙

- README는 현재 구현 상태와 남은 공백을 분리해서 적는다.
- `notion/`도 레포에 포함되는 공개 백업 문서로 본다.
- 다만 빠른 진입과 최신 상태 확인은 README와 `docs/`를 먼저 읽는 것이 좋다.
- `notion/`을 다시 쓰고 싶다면 기존 폴더를 `notion-archive/`로 이름만 바꿔 보존한다.
- `.venv`, `node_modules`, `dist`, `__pycache__`, local DB 같은 생성물은 source content로 취급하지 않는다.

## 검증 스냅샷

- `08/v0`: `UV_PYTHON=python3.12 make gate-all`
- `08/v1`: `UV_PYTHON=python3.12 make gate-all`, `UV_PYTHON=python3.12 make smoke-postgres`
- `08/v2`: `UV_PYTHON=python3.12 make gate-all`, `UV_PYTHON=python3.12 make smoke-postgres`
- `08/v3`: `UV_PYTHON=python3.12 make gate-all`, `pnpm test --run`, `docker compose config`
- `00~07/python`: 각 stage-local `uv run pytest -q`
- `07/react`: `pnpm test --run`

## 범위 밖

- 실제 운영 계정으로 Upstage, OpenAI, Langfuse를 호출하는 검증
- multi-tenant SaaS
- SSO, billing, 조직 관리 기능

## 읽는 사람에게 미리 말해 둘 점

- `notion/`은 권위 문서가 아니라 과정과 배움을 보존하는 백업 문서다.
- proof artifact의 PNG 스크린샷은 보조 자료이고, 핵심 검증 근거는 JSON, 텍스트 artifact, 테스트 결과다.

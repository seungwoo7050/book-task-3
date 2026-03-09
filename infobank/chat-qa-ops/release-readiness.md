# Study2 Release Readiness

`study2/`는 학습용 저장소이지만, 현재 상태는 공개 원격 저장소에 올려도 이해 가능한 구조와 재현 가능한 검증 경로를 갖추는 것을 목표로 정리했다.

## Public Scope

- 주제: 한국어 챗봇 상담 품질 관리
- 목표: rule/guardrail, evidence verification, judge scoring, golden regression, monitoring UI를 단계적으로 학습하고 최종적으로 QA Ops capstone demo로 묶는다.
- 공개 대상: tracked 문서, stage implementation pack, capstone snapshot, proof artifact
- 비공개 대상: `notion/` 작업 노트

## What Is Included

- `00~07`: capstone에서 개념을 잘라낸 학습용 implementation pack
- `08-capstone-submission/v0`: runnable baseline snapshot
- `08-capstone-submission/v1`: regression hardening, provider chain, lineage/trace, PostgreSQL smoke path
- `08-capstone-submission/v2`: retrieval improvement experiment and compare proof

## Public Hygiene Rules Applied

- `legacy/`는 수정하지 않았다.
- `study2/**/notion`은 로컬 전용으로 유지한다.
- `.venv`, `node_modules`, `dist`, `__pycache__`, local DB, local Chroma persistence, egg-info는 source content로 취급하지 않는다.
- README는 현재 구현과 staged gap을 구분해서 쓴다.

## Verification Snapshot

- `08/v0`: `UV_PYTHON=python3.12 make gate-all`
- `08/v1`: `UV_PYTHON=python3.12 make gate-all`, `UV_PYTHON=python3.12 make smoke-postgres`
- `08/v2`: `UV_PYTHON=python3.12 make gate-all`, `UV_PYTHON=python3.12 make smoke-postgres`
- `07/react`: `pnpm test --run`
- `00~07/python`: 각 stage-local `uv run pytest -q`

## Known Non-Goals

- 실제 운영 계정으로 Upstage/OpenAI/Langfuse를 호출하는 검증은 포함하지 않는다.
- `notion/` 내용은 공개 저장소의 권위 문서가 아니다.
- proof artifact의 PNG 스크린샷은 문서 보조 자료이며, 핵심 검증 근거는 JSON/text artifact와 테스트 결과다.

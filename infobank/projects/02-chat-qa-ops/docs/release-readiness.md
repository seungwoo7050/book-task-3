# Chat QA Ops 공개 정리 기준

이 문서는 `projects/02-chat-qa-ops/`를 공개 저장소 기준으로 어떻게 읽고 검증하는지 한 장으로 요약한다.

## 공개 범위

- 주제: 한국어 챗봇 상담 품질 관리
- 공식 답: `capstone/v2-submission-polish`
- 확장 답: `capstone/v3-self-hosted-oss`
- 학습 근거: `stages/00~07`, `docs/verification-matrix.md`, `capstone/notion/05-development-timeline.md`

## 무엇이 들어 있는가

- `stages/00~07`: 계약과 검증 단위를 나눈 학습 pack
- `capstone/v0`: runnable baseline snapshot
- `capstone/v1`: regression hardening, provider chain, lineage/trace, PostgreSQL smoke path
- `capstone/v2`: retrieval improvement experiment와 compare proof를 갖춘 공식 제출 답
- `capstone/v3`: self-hosted OSS 확장 버전

## 검증 스냅샷

- 공식 답 준비: `cd capstone/v2-submission-polish/python && UV_PYTHON=python3.12 uv sync --extra dev`
- 공식 답: `cd capstone/v2-submission-polish/python && UV_PYTHON=python3.12 make gate-all`
- smoke path: `cd capstone/v2-submission-polish/python && UV_PYTHON=python3.12 make smoke-postgres`
- 확장 답: `cd capstone/v3-self-hosted-oss/python && UV_PYTHON=python3.12 make gate-all`

## 기억할 점

- README와 `docs/`가 front door이고, `notion/`은 판단 과정과 재현 경로를 남기는 공개 노트다.
- `notion-archive/`는 pre-migration 경로 기준 기록을 보존하는 역사 문서다.

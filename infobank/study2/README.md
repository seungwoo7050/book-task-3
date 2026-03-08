# Study 2

주제는 챗봇 상담 품질 관리다.
세 과제 중 현재 구현 우선순위가 가장 높고, 실제 runnable 데모와 제출물은 이 트랙을 기준으로 관리한다.

## Active Track

- 목표: 상담 챗봇 자체가 아니라 상담 품질을 정의, 자동 평가, 모니터링하는 QA Ops 계층을 만든다.
- 제출 전략: 가장 먼저 `v0` 제출 가능 데모를 닫고, 이후 폴더 복제 방식으로 확장한다.
- 주력 스택: `Python 3.12 + FastAPI + Pydantic + SQLAlchemy`, `React + Vite`, `PostgreSQL`, `Langfuse`
- 모델 어댑터: `Upstage Solar` 우선, `OpenAI` 보조, `Ollama` fallback
- 배포/운영 기본 설명: `AWS Seoul`

## Sequence

`00-source-brief` -> `01-quality-rubric-and-score-contract` -> `02-domain-fixtures-and-chat-harness` -> `03-rule-and-guardrail-engine` -> `04-claim-and-evidence-pipeline` -> `05-judge-and-score-merge` -> `06-golden-set-and-regression` -> `07-monitoring-dashboard-and-review-console` -> `08-capstone-submission`

## Current State

- `00~07`: 각 단계에 실제 implementation pack을 추가했다. `00~06`은 집중 Python pack, `07`은 FastAPI snapshot API + React dashboard slice다.
- `08/v0`: `SQLite + heuristic` runnable snapshot으로 정리했다. replay fixture, escalation rule, dependency health 정규화가 반영됐다.
- `08/v1`: provider chain, run lineage, trace payload, dashboard compare, PostgreSQL smoke path가 구현됐다.
- `08/v2`: `retrieval-v2` 실험이 들어갔고, 같은 `golden-set`에서 `v1.0 -> v1.1` 비교 결과 `avg_score 84.06 -> 87.76`, `critical 2 -> 0`, `pass 16 -> 19`, `fail 14 -> 11`을 재현했다.
- `08/v3`: `v2`를 single-team self-hosted OSS snapshot으로 승격했다. 로그인, transcript JSONL 업로드, KB ZIP 업로드, 비동기 job, run-scoped dashboard/session review, Docker Compose quickstart를 제공한다.

## Notes

- `legacy/`는 읽기 전용 참조로 유지했다.
- `notion/` 5종 문서는 `00~08` 모두 생성했다. tracked 문서는 notion 의존 없이 읽히도록 유지했다.
- 공개 저장소 마감 기준은 [`release-readiness.md`](/Users/woopinbell/work/chat-bot/study2/release-readiness.md)에 정리했다.
- self-hosted 사용자는 `study2/08-capstone-submission/v3-self-hosted-oss`부터 시작하면 되고, `v0~v2`는 제출 이력과 비교 증빙용 archive로 본다.

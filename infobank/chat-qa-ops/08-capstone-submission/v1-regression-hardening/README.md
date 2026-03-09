# Study 2 Capstone v1

`v1-regression-hardening`은 `v0-initial-demo`를 폴더 단위로 복제한 확장 버전이다.

## Implemented Delta

- golden set 커버리지 확대
- run-level 회귀 검증과 version compare 강화
- Upstage Solar -> OpenAI -> Ollama provider chain 추가
- dependency health와 fallback 경로 안정화
- Langfuse lineage/trace envelope 준비
- PostgreSQL smoke path와 SQLite fallback 정리

## Verification Snapshot

- `UV_PYTHON=python3.12 make gate-all`
- `UV_PYTHON=python3.12 make smoke-postgres`

현재 내용은 `v0`를 기반으로 하되, trace 노출과 운영 검증을 실제 구현 상태까지 끌어올린 버전이다.

## Presentation Material

- 발표용 문서는 [`docs/presentation/v1-demo-presentation.md`](/Users/woopinbell/work/chat-bot/study2/08-capstone-submission/v1-regression-hardening/docs/presentation/v1-demo-presentation.md)에 정리했다.

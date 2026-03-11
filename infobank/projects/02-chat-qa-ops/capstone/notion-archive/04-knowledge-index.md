> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../docs/catalog/path-migration-map.md)를 본다.

# Capstone — 지식 인덱스

## 버전별 기술 스택

| 항목 | v0 | v1 | v2 | v3 |
|------|----|----|----|----|
| DB | SQLite | SQLite + PostgreSQL smoke | PostgreSQL | PostgreSQL |
| Judge | heuristic | provider chain (Solar→OpenAI→Ollama→heuristic) | provider chain | provider chain |
| Retrieval | keyword | keyword | keyword + alias/category/risk rerank | keyword + rerank |
| Auth | 없음 | 없음 | 없음 | single admin (email/password) |
| 배포 | 로컬 실행 | 로컬 실행 | 로컬 실행 | Docker Compose |
| Trace | 없음 | Langfuse 준비 | Langfuse 준비 | Langfuse 연동 |

## 핵심 개념

| 개념 | 설명 |
|------|------|
| provider chain | LLM provider가 실패하면 다음 provider로 넘어가는 fallback 체인. 최종 fallback은 heuristic |
| retrieval-v2 | alias 매핑, category 필터, risk rerank를 추가한 개선된 검색 로직 |
| compare artifact | baseline과 candidate의 golden set 실행 결과를 비교한 JSON 문서 |
| lineage | 각 평가의 실행 환경 메타: run_label, dataset, trace_id, retrieval_version |
| judge_trace | 어떤 provider/model로 채점했는지, short_circuit 발생 여부 |
| evaluation job | v3에서 도입. 평가 요청을 큐에 넣고 worker가 비동기 처리 |
| KB bundle | Knowledge Base 문서들을 ZIP으로 묶어서 업로드하는 방식 (v3) |

## 품질 지표 변화

```
v1 (baseline)        →  v2 (candidate)
avg_score: 84.06     →  87.76  (+3.7)
critical:  2         →  0      (-2)
pass:      16        →  19     (+3)
fail:      14        →  11     (-3)
```

## 실행 명령어 요약

| 목적 | 명령어 |
|------|--------|
| v0 백엔드 테스트 | `cd v0-initial-demo/python && uv sync --extra dev && make test-backend` |
| v1 전체 게이트 | `cd v1-regression-hardening/python && UV_PYTHON=python3.12 make gate-all` |
| v1 PostgreSQL 테스트 | `UV_PYTHON=python3.12 make smoke-postgres` |
| v3 Docker 실행 | `cd v3-self-hosted-oss && docker compose up --build` |
| v3 AI 프로필 | `docker compose --profile ai up --build` |
| React 테스트 (모든 버전) | `cd react && pnpm install && pnpm test --run` |

## 다음 단계 (범위 밖)

- multi-tenant / RBAC / SSO
- Redis/Celery 기반 job queue (현재 in-process worker)
- Kubernetes 배포
- billing / usage metering

> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Source Brief — 지식 인덱스

## 핵심 개념

| 개념 | 설명 | 관련 파일 |
|------|------|-----------|
| MCP (Model Context Protocol) | LLM이 외부 도구를 호출하기 위한 표준 프로토콜 | 전체 프로젝트 |
| catalog | MCP 도구 목록. 각 도구의 이름, 버전, 카테고리, 한국어 노출 필드를 포함 | `shared/src/catalog.ts` |
| manifest | MCP 도구의 메타데이터 스키마. Zod로 정의된 입출력 계약 | `shared/src/contracts.ts` |
| eval fixture | 추천 알고리즘의 정확도를 측정하기 위한 테스트 케이스 모음 | `shared/src/eval.ts` |
| reference spine | 프로젝트 전체를 관통하는 참조 문서 목록 | `docs/reference-spine.md` |
| 한국어 노출 | 도구 추천 시 한국어로 표시되는 tagline, description, differentiator | `catalog.ts → exposure.ko` |

## 프로젝트 구조

```
mcp-recommendation-demo/
  00-source-brief → 07-operator-dashboard  (stage별 문서)
  08-capstone-submission/
    v0-initial-demo/     — baseline selector + offline eval
    v1-ranking-hardening/ — reranker + feedback + compare
    v2-submission-polish/ — gate + release + artifact
    v3-oss-hardening/     — auth + RBAC + Docker Compose
```

## 기술 스택

- **Backend**: Node.js, TypeScript, Fastify, Drizzle ORM, PostgreSQL
- **Frontend**: Next.js, React, TypeScript
- **Schema**: Zod (runtime validation)
- **패키지 관리**: pnpm (workspace)
- **테스트**: Vitest (unit), Playwright (e2e)
- **빌드**: TypeScript compiler, Next.js

## 다음 단계 연결

- **stage 01**: catalog의 도구를 어떤 기준으로 평가(rubric)하고, eval contract를 어떻게 정의할지

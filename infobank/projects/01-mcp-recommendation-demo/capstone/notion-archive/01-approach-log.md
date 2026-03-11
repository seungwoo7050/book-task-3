> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../docs/catalog/path-migration-map.md)를 본다.

# 01 — 접근 기록: v0에서 v3까지의 구현 여정

## v0 — 기반 구축: "일단 추천이 되게 하자"

### 패키지 구조 결정

pnpm workspace를 세 패키지로 나눴다:

```
shared/   → Zod 스키마, seed catalog, eval fixtures
node/     → Fastify API 서버, Drizzle + PostgreSQL
react/    → Next.js App Router 운영 콘솔
```

`shared`를 독립 패키지로 빼는 것이 핵심이었다.  
API와 프론트엔드가 같은 타입을 import하게 되면 컨트랙트 불일치가 원천적으로 사라진다.

### Zod 스키마 중심 설계

`mcpManifestSchema`, `catalogEntrySchema`, `recommendationRequestSchema`를 먼저 정의했다.  
API 라우트는 이 스키마로 요청을 검증하고, 프론트엔드는 추론된 타입을 import한다.

### Baseline Selector

추천 로직의 첫 번째 버전은 단순하다:

1. catalog에서 `desiredCapabilities`와 매칭되는 도구를 필터링
2. `freshnessScore`와 capability overlap으로 점수를 계산
3. 한국어 `explanationKo`를 생성 — "X는 Y 역량이 직접 맞습니다" 패턴

### Offline Eval

golden set(`eval.ts`)에 기대 결과를 미리 정의해두고:
- top-3 recall: 정답이 상위 3개 안에 들어가는 비율
- explanation completeness: 한국어 설명이 빈 문자열이 아닌 비율
- forbidden hit rate: 금지 도구가 추천에 포함된 비율

이 세 지표가 이후 모든 버전에서 동일하게 측정된다.

## v1 — 신호 기반 Reranking

### Signal-Rerank 전략

v0의 baseline이 "정적 메타데이터"만 보는 한계를 깨기 위해,  
usage log와 feedback을 추천 점수에 반영하는 reranker를 추가했다.

reranker의 핵심 아이디어:
- accept가 많은 도구 → 점수 상승
- dismiss가 많은 도구 → 점수 하락
- feedback의 `scoreDelta` → 직접 점수 보정

### Baseline/Candidate Compare

같은 query에 대해 baseline과 candidate를 동시에 실행하고:
- nDCG@3: 정규화된 할인 누적 이득 (위치가 중요)
- Top-1 hit rate: 첫 번째 추천이 정답인 비율
- Uplift: candidate nDCG@3 - baseline nDCG@3

이 compare 결과를 대시보드에서 실시간으로 확인할 수 있게 했다.

### Catalog & Experiment CRUD

운영자가 대시보드에서:
- MCP 도구를 추가·수정·삭제
- A/B 실험을 생성·토글·삭제

이로써 "코드를 건드리지 않고 실험을 운영"하는 흐름이 완성되었다.

## v2 — 릴리즈 품질 게이트

### Release Candidate 개념 도입

MCP 도구 하나가 릴리즈되기 전에 "Release Candidate"로 관리한다.  
RC에는 `previousVersion`, `releaseVersion`, `targetClientVersion`, `requiredDocs`, `requiredArtifacts`가 포함된다.

### Compatibility Gate

RC의 manifest를 분석해서:
- 현재 semver가 이전 버전과 호환되는가
- `testedClientVersions`가 target을 포함하는가
- deprecated field를 사용하고 있지 않은가

결과: `COMPATIBLE / INCOMPATIBLE / UNKNOWN`

### Release Gate

compatibility + eval + compare 결과를 종합해서 최종 `PASS / FAIL / MANUAL_REVIEW` 판정.  
check별로 pass/fail 상세 이유를 기록한다:
- evalRecallAboveThreshold (eval top-3 recall ≥ 0.8)
- upliftNonNegative (compare uplift ≥ 0)
- compatibilityPass (compatibility gate COMPATIBLE)
- noForbiddenHits (forbidden hit rate = 0)
- requiredDocsComplete (필요 문서 존재 확인)

### Artifact Export

gate 결과를 JSON 파일로 추출한다.  
이것은 "이 MCP가 왜 릴리즈 가능한지" 증거를 외부 시스템에 전달하기 위한 것이다.

## v3 — Self-Hosted OSS

### Auth / RBAC

세 가지 역할:
- **owner**: 모든 작업 가능, 사용자 관리, 설정 변경
- **operator**: catalog CRUD, 실험 관리, 추천 실행, feedback
- **viewer**: 읽기 전용, 대시보드 조회만 가능

이메일·비밀번호 기반 인증, 세션 쿠키(httpOnly)로 상태 유지.  
`resolveAuth()` 미들웨어가 모든 API 라우트 앞에서 권한을 체크한다.

### pg-boss Worker

eval, compare, compatibility, release gate, artifact export — 이 5개 작업이 시간이 걸릴 수 있다.  
v2까지는 동기적으로 API 응답을 기다렸지만, v3에서는 pg-boss로 비동기 job queue를 도입했다.

1. API가 job을 enqueue
2. Worker 프로세스가 dequeue → 실행 → 결과 저장
3. 대시보드에서 job 상태를 polling

### Audit Log

"누가 언제 무엇을 했는가"를 기록한다:
- catalog 생성/수정/삭제
- experiment 토글
- release candidate 상태 변경
- 로그인/로그아웃

### Docker Compose

4개 서비스:
- `postgres`: PostgreSQL 17 Alpine
- `api`: Fastify 서버 (마이그레이션 실행 후 부팅)
- `worker`: pg-boss consumer
- `web`: Next.js 운영 콘솔

`docker compose up -d --build` 한 번으로 전체 시스템이 올라간다.

## 아키텍처 결정의 핵심 근거

| 결정 | 대안 | 선택 이유 |
|------|------|-----------|
| 단일 모노레포 | 별도 리포지토리 | shared 타입 동기화 비용 제거 |
| Drizzle (not Prisma) | Prisma | codegen 없음, SQL에 가까움 |
| pg-boss (not BullMQ) | BullMQ + Redis | PostgreSQL만으로 충족, 추가 인프라 불필요 |
| 쿠키 세션 (not JWT) | JWT | 서버 사이드 무효화 가능, CSRF 방어 용이 |
| Docker Compose (not K8s) | Kubernetes | self-hosted 단일 노드 시나리오에 적합 |

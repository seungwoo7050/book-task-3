> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../docs/catalog/path-migration-map.md)를 본다.

# 04 — 지식 인덱스: 전체 스택 참조표

## v0 → v3 비교표

| 항목 | v0 | v1 | v2 | v3 |
|------|----|----|----|----|
| API 포트 | 3100 | 3101 | 3102 | 3103 |
| Web 포트 | 3000 | 3001 | 3002 | 3003 |
| DB | PostgreSQL | PostgreSQL | PostgreSQL | PostgreSQL |
| 추천 전략 | baseline | baseline + candidate | baseline + candidate | baseline + candidate |
| Reranker | ❌ | signal-rerank | signal-rerank | signal-rerank |
| Usage Log | ❌ | ✅ | ✅ | ✅ |
| Feedback | ❌ | ✅ | ✅ | ✅ |
| Compare | ❌ | ✅ | ✅ | ✅ |
| Experiment CRUD | ❌ | ✅ | ✅ | ✅ |
| Catalog CRUD | seed only | ✅ | ✅ | ✅ + import/export |
| Compatibility Gate | ❌ | ❌ | ✅ | ✅ (job) |
| Release Gate | ❌ | ❌ | ✅ | ✅ (job) |
| Artifact Export | ❌ | ❌ | ✅ | ✅ (job) |
| Release Candidate | ❌ | ❌ | ✅ | ✅ |
| Auth / RBAC | ❌ | ❌ | ❌ | ✅ |
| Background Worker | ❌ | ❌ | ❌ | pg-boss |
| Audit Log | ❌ | ❌ | ❌ | ✅ |
| Docker Compose | ❌ | ❌ | ❌ | ✅ |

## 패키지 구조 (전 버전 공통)

```
v{n}/
├── shared/          # Zod 스키마, seed data, eval fixtures
│   └── src/
│       ├── contracts.ts    # 모든 스키마 정의
│       ├── catalog.ts      # seed MCP 도구 10+개
│       └── eval.ts         # offline eval golden set
├── node/            # Fastify API 서버
│   └── src/
│       ├── app.ts          # 라우트 정의
│       ├── server.ts       # 서버 부팅
│       ├── config.ts       # 환경변수
│       ├── db/             # Drizzle schema + migration
│       ├── repositories/   # DB 접근 계층
│       └── services/       # 비즈니스 로직
├── react/           # Next.js 운영 콘솔
│   └── components/
│       └── mcp-dashboard.tsx
├── tests/           # Vitest unit + Playwright e2e
├── package.json
├── pnpm-workspace.yaml
└── tsconfig.base.json
```

### v3 추가 파일

```
v3/
├── Dockerfile.api
├── Dockerfile.web
├── Dockerfile.worker
├── docker-compose.yml
├── .env.example
├── CONTRIBUTING.md
├── SECURITY.md
├── node/src/
│   ├── worker.ts           # pg-boss consumer
│   ├── services/
│   │   ├── auth-service.ts     # 인증·세션
│   │   ├── audit-service.ts    # 감사 로그
│   │   ├── instance-service.ts # 인스턴스 설정
│   │   └── job-service.ts      # pg-boss enqueue
│   └── scripts/
│       └── bootstrap-owner.ts  # owner 계정 초기화
└── scripts/
    └── capture-presentation.ts
```

## 핵심 Zod 스키마 (shared/src/contracts.ts)

### 전 버전 공통

| 스키마 | 역할 |
|--------|------|
| `mcpManifestSchema` | MCP 도구의 manifest 구조 |
| `catalogEntrySchema` | manifest + 메타데이터 (freshnessScore, exposure 등) |
| `recommendationRequestSchema` | 추천 요청 (query, desiredCapabilities, environment) |
| `reasonTraceSchema` | 추천 이유 trace (base score + boost breakdown) |
| `offlineEvalCaseSchema` | golden set eval case (expected rankings) |

### v1 추가

| 스키마 | 역할 |
|--------|------|
| `experimentConfigSchema` | A/B 실험 설정 |
| `feedbackRecordSchema` | 운영자 피드백 |
| `usageEventSchema` | impression/click/accept/dismiss 이벤트 |

### v2 추가

| 스키마 | 역할 |
|--------|------|
| `releaseCandidateSchema` | RC lifecycle |
| `compatibilityReportSchema` | semver 호환성 분석 |
| `releaseGateReportSchema` | 릴리즈 품질 게이트 |
| `artifactExportSchema` | 제출용 JSON 증빙 |

### v3 추가

| 스키마 | 역할 |
|--------|------|
| `authLoginRequestSchema` | 로그인 요청 |
| `authSessionResponseSchema` | 세션 응답 |
| `publicUserSchema` | 공개 사용자 정보 |
| `createUserRequestSchema` | 사용자 생성 |
| `updateUserRequestSchema` | 사용자 수정 |
| `updateSettingsRequestSchema` | 인스턴스 설정 |
| `jobNameSchema` | pg-boss job 이름 (enum) |
| `jobRunSchema` | job 실행 기록 |
| `jobEnqueueResponseSchema` | enqueue 응답 |
| `catalogImportBundleSchema` | catalog import/export 번들 |

## API 엔드포인트 누적

### v0 (4개)

```
GET  /api/catalog
POST /api/recommendations
POST /api/evals/run
GET  /api/evals/latest
```

### v1 추가 (8개 → 총 12개)

```
POST /api/recommendations/candidate
GET/POST/PUT/DELETE /api/experiments
GET/POST /api/usage-events
POST /api/feedback
GET  /api/compare/latest
POST /api/compare/run
```

### v2 추가 (8개 → 총 20개)

```
GET/POST/PUT/DELETE /api/release-candidates
GET  /api/compatibility/latest
POST /api/compatibility/run
GET  /api/release-gate/latest
POST /api/release-gate/run
GET  /api/submission/latest
POST /api/submission/export
```

### v3 추가 (12개 → 총 32개)

```
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
GET/POST /api/users
PUT  /api/users/:id
GET/PUT /api/settings
POST /api/catalog/import
GET  /api/catalog/export
GET  /api/audit-events
GET  /api/jobs/recent
POST /api/jobs/enqueue
```

## 기본 계정 (v3)

| 역할 | 이메일 | 비밀번호 |
|------|--------|----------|
| owner | owner@study1.local | ChangeMe123! |
| operator | operator@study1.local | Operator123! |
| viewer | viewer@study1.local | Viewer123! |

## Docker Compose 서비스 (v3)

| 서비스 | 이미지 | 포트 | 의존 |
|--------|--------|------|------|
| postgres | postgres:17-alpine | 5543:5432 | - |
| api | Dockerfile.api | 3103:3103 | postgres (healthy) |
| worker | Dockerfile.worker | - | postgres (healthy), api (started) |
| web | Dockerfile.web | 3003:3003 | api (started) |

## 테스트 구성

| 명령 | 대상 | 도구 |
|------|------|------|
| `pnpm test` | unit + UI | Vitest |
| `pnpm test:integration` | DB 연동 라우트 | Vitest (DB 필요) |
| `pnpm eval` | offline eval | 커스텀 스크립트 |
| `pnpm compare` | baseline vs candidate | 커스텀 스크립트 |
| `pnpm e2e` | 대시보드 흐름 | Playwright |

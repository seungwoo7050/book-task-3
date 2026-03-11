> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Usage Logs, Metrics & Feedback Loop — 개발 타임라인

## 1단계: DB schema 추가

```bash
cd 08-capstone-submission/v1-ranking-hardening/node/src/db
# schema.ts에 usageEvents, feedbackRecords, experiments 테이블 정의 추가
```

```bash
pnpm migrate  # 새 테이블 생성
```

Drizzle의 마이그레이션은 `drizzle-kit generate` → `drizzle-kit push` 순서로 실행한다.

## 2단계: usage event API

```bash
# app.ts에 POST /api/usage-events 라우트 추가
```

Zod schema로 request body 검증:

```typescript
const usageEventSchema = z.object({
  toolId: z.string(),
  recommendationId: z.string().optional(),
  experimentId: z.string().optional(),
  action: z.enum(['selected', 'executed', 'dismissed'])
});
```

## 3단계: feedback API

```bash
# app.ts에 POST /api/feedback 라우트 추가
```

```typescript
const feedbackSchema = z.object({
  toolId: z.string(),
  usageEventId: z.number().optional(),
  score: z.number().int().min(1).max(5),
  comment: z.string().optional()
});
```

## 4단계: experiment CRUD

```bash
# app.ts에 GET/POST /api/experiments, PATCH /api/experiments/:id 추가
```

상태 전이 제어를 route handler에 구현:
- draft → running: OK
- running → completed: OK
- 그 외: 400

## 5단계: catalog CRUD

```bash
cd node/src/repositories
touch catalog-repository.ts
```

기존 seed-only였던 catalog에 create/update/delete를 추가했다.
`POST /api/catalog`, `PUT /api/catalog/:id`, `DELETE /api/catalog/:id`

## 6단계: 대시보드 UI 업데이트

```bash
cd react/components
# mcp-dashboard.tsx에 experiment 관리 + catalog CRUD 폼 추가
```

```bash
cd react
pnpm dev  # 시각적 확인
```

## 7단계: 테스트

```bash
pnpm test  # unit test
pnpm e2e   # Playwright e2e test
```

## 비고

- 이 stage는 v1 capstone에서 구현된다. v0에는 usage/feedback 기능이 없다.
- experiment CRUD는 대시보드에서도 API에서도 가능하다.
- `pnpm seed`를 다시 실행하면 seed 데이터에 일부 usage event가 포함된다.

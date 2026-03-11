> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Usage Logs, Metrics & Feedback Loop — 접근 기록

## DB 테이블 설계

Drizzle ORM으로 세 개의 테이블을 추가했다:

### usage_events

```typescript
export const usageEvents = pgTable('usage_events', {
  id: serial('id').primaryKey(),
  toolId: varchar('tool_id').notNull(),
  recommendationId: varchar('recommendation_id'),
  experimentId: varchar('experiment_id'),
  action: varchar('action').notNull(),  // 'selected' | 'executed' | 'dismissed'
  createdAt: timestamp('created_at').defaultNow()
});
```

### feedback_records

```typescript
export const feedbackRecords = pgTable('feedback_records', {
  id: serial('id').primaryKey(),
  toolId: varchar('tool_id').notNull(),
  usageEventId: integer('usage_event_id'),
  score: integer('score').notNull(),  // 1~5
  comment: text('comment'),
  createdAt: timestamp('created_at').defaultNow()
});
```

### experiments

```typescript
export const experiments = pgTable('experiments', {
  id: varchar('id').primaryKey(),
  name: varchar('name').notNull(),
  selectorType: varchar('selector_type').notNull(),  // 'baseline' | 'reranker'
  status: varchar('status').notNull(),  // 'draft' | 'running' | 'completed'
  startedAt: timestamp('started_at'),
  endedAt: timestamp('ended_at')
});
```

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/api/usage-events` | POST | usage event 기록 |
| `/api/feedback` | POST | feedback 기록 |
| `/api/experiments` | GET | 실험 목록 |
| `/api/experiments` | POST | 실험 생성 |
| `/api/experiments/:id` | PATCH | 실험 상태 변경 |
| `/api/metrics/tool/:id` | GET | 도구별 usage/feedback 요약 |

## catalog CRUD 추가

v1에서 catalog-repository.ts에 CRUD를 추가했다.
이전에는 seed만 있었지만, 이제 대시보드에서 도구를 추가/수정/삭제할 수 있다.

mcp-dashboard.tsx에서 catalog 목록 + CRUD 폼을 표시한다.

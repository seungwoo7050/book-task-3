> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Registry Catalog & Manifest Schema — 개발 타임라인

## 1단계: contracts.ts에 manifest schema 확정

```bash
cd shared/src
# contracts.ts 편집 — mcpManifestSchema, catalogEntrySchema 정의
```

Zod schema를 정의한 후 `z.infer<typeof mcpManifestSchema>`로 TypeScript 타입을 추출했다.
이렇게 하면 schema와 타입이 항상 동기화된다.

## 2단계: catalog.ts 작성

```bash
touch shared/src/catalog.ts
```

10+ MCP 도구를 하드코딩했다.
각 도구가 mcpManifestSchema를 통과하는지 빌드 시 타입 체크로 확인된다.

```bash
cd shared
pnpm tsc --noEmit  # 타입 체크
```

## 3단계: DB schema 정의 (Drizzle)

```bash
cd 08-capstone-submission/v0-initial-demo/node/src/db
touch schema.ts
```

Drizzle ORM으로 PostgreSQL 테이블을 정의했다:

```typescript
export const catalogTable = pgTable('catalog', {
  id: serial('id').primaryKey(),
  name: varchar('name', { length: 255 }).unique().notNull(),
  version: varchar('version', { length: 50 }).notNull(),
  category: varchar('category', { length: 100 }).notNull(),
  // ...
});
```

```bash
pnpm migrate  # DB 마이그레이션 실행
```

## 4단계: seed.ts 구현

```bash
cd node/src/scripts
touch seed.ts
```

```bash
pnpm seed
# ✓ Seeded 12 catalog entries
```

upsert 패턴으로 구현하여 반복 실행 가능.

## 5단계: manifest validation route 추가

```bash
# app.ts에 POST /api/manifests/validate 라우트 추가
```

Fastify 라우트에서 request body를 Zod로 파싱:

```typescript
app.post('/api/manifests/validate', async (request, reply) => {
  const result = mcpManifestSchema.safeParse(request.body);
  return { valid: result.success, errors: result.error?.issues };
});
```

## 6단계: 테스트

```bash
cd node
pnpm test
```

manifest-validation.test.ts:
- 올바른 manifest → `{ valid: true }`
- 필수 필드 누락 → `{ valid: false, errors: [...] }`
- optional 필드 없음 → `{ valid: true }`

## 비고

- `pnpm seed`는 `pnpm migrate` 후에 실행해야 한다.
- DB가 없으면 `pnpm db:up`으로 PostgreSQL Docker 컨테이너를 먼저 시작한다.
- seed 데이터 변경 시 eval 결과가 달라질 수 있으므로, 변경 후 `pnpm eval`로 영향을 확인한다.

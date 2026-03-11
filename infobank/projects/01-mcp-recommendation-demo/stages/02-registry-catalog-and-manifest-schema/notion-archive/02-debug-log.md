> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Registry Catalog & Manifest Schema — 디버그 기록

## seed 중복 삽입 문제

### 상황

최초 seed.ts 구현에서 `INSERT` 를 사용했다.
`pnpm seed`를 두 번 실행하면 unique constraint violation이 발생했다.

### 해결

Drizzle의 `onConflictDoUpdate`를 사용하여 upsert 패턴으로 변경:

```typescript
await db.insert(catalogTable)
  .values(entry)
  .onConflictDoUpdate({
    target: catalogTable.name,
    set: { ...entry, updatedAt: new Date() }
  });
```

name을 unique key로 사용하므로, 같은 이름의 도구가 있으면 업데이트한다.

## manifest validation에서 optional 필드 처리

### 상황

exposure.ko 필드가 없는 manifest를 validate했을 때,
Zod가 에러를 반환하지 않아야 하는데 반환했다.

원인: `exposure`를 `z.object({ ko: ... })`로 정의했는데,
`exposure` 자체를 `.optional()`로 감싸지 않았다.

### 해결

```typescript
exposure: z.object({
  ko: z.object({
    tagline: z.string(),
    description: z.string(),
    differentiator: z.string().optional()
  })
}).optional()
```

`exposure` 전체를 optional로, 그 안의 `differentiator`도 optional로 변경했다.

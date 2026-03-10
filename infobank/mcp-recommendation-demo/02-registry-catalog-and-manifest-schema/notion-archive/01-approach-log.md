# Registry Catalog & Manifest Schema — 접근 기록

## Zod manifest contract 설계

manifest schema의 필수 필드를 결정해야 했다.

필수:
- `name`: 도구 고유 이름 (slug 형식)
- `version`: semver 형식 (compatibility gate에서 사용)
- `category`: dev-tools, data, docs, monitoring 등
- `description`: 영문 도구 설명
- `inputs`: 도구 입력 파라미터 스키마
- `outputs`: 도구 출력 파라미터 스키마

선택:
- `exposure.ko`: 한국어 노출 필드 (stage 03에서 설계)
- `status`: active, deprecated, experimental
- `compatibility`: 다른 도구와의 호환성 정보

Zod의 `.optional()`과 `.default()`를 적절히 사용하여,
필수 필드 누락 시 바로 에러를 반환하도록 했다.

## seed 스크립트(seed.ts) 설계

seed.ts의 역할:
1. catalog.ts에서 도구 목록을 import
2. Drizzle ORM으로 DB에 upsert (이미 있으면 업데이트, 없으면 삽입)
3. seed 완료 후 삽입된 도구 수를 출력

upsert를 쓴 이유: `pnpm seed`를 여러 번 실행해도 중복이 생기지 않아야 한다.

```bash
pnpm seed
# ✓ Seeded 12 catalog entries
```

## manifest validation route

`POST /api/manifests/validate` 엔드포인트:
- body에 manifest JSON을 받는다
- Zod schema로 파싱한다
- 성공: `{ valid: true }`
- 실패: `{ valid: false, errors: [...] }`

Fastify의 schema validation과 별도로 Zod를 사용한 이유:
Fastify JSON Schema는 OpenAPI 호환이지만, TypeScript 타입 추론이 약하다.
Zod는 schema에서 타입을 추론하므로, 서비스 레이어에서 타입 안전성을 유지할 수 있다.

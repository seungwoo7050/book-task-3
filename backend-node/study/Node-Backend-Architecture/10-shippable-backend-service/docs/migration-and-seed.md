# Migration And Seed

## migration 정책

- `synchronize: true`를 사용하지 않는다.
- schema는 `src/database/migrations/1710000000000-initial-schema.ts`에 체크인한다.
- 로컬과 CI 모두 `pnpm run db:migrate`를 기준 경로로 사용한다.

## seed 정책

- `pnpm run db:seed`는 아래 데이터를 준비한다.
  - admin 계정: `admin / admin123`
  - demo books 2권
- seed는 이미 같은 데이터가 있으면 중복 생성하지 않는다.

## 왜 migration 기반으로 바꿨는가

- `09`의 SQLite `synchronize` 모드는 학습용으로는 빠르지만 실무 제출용 예제로는 약하다.
- Postgres migration을 체크인해 두면 schema 변경 이력을 설명할 수 있다.
- seed script가 있으면 reviewer가 API 시나리오를 재현하기 쉽다.

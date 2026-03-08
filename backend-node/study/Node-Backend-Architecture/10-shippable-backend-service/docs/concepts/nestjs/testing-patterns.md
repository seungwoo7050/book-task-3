# Testing Patterns

## 단위 테스트

- `AuthService`
  - 중복 username
  - JWT 발급
  - invalid credential
  - throttling 임계치 도달
- `BooksService`
  - create/update/delete event
  - cache write
  - cache invalidation
  - not found

## e2e 테스트

- health/live, health/ready
- Swagger `/docs`
- register/login
- throttling
- public books read
- admin write / regular-user forbid
- validation / 404
- Redis cache hit 전제와 invalidation

## 검증 순서

1. `pnpm run build`
2. `pnpm run test`
3. `docker compose up -d postgres redis`
4. `pnpm run test:e2e`

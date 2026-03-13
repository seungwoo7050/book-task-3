# 10-shippable-backend-service evidence ledger

이 프로젝트의 path 단위 `git log`도 `2026-03-12` 이관 커밋 하나로만 남아 있다. chronology는 bootstrap, auth/cache/runtime/DB 코드, unit/e2e tests, 실제 compose 기반 재검증 CLI를 기준으로 다시 세운 것이다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | capstone을 제출용 서비스 표면으로 다시 포장한다 | `nestjs/src/app.bootstrap.ts`, `database/migrations/1710000000000-initial-schema.ts` | capstone에 README만 보강하면 제출용 서비스처럼 읽힐 것 같았다 | global bootstrap, Swagger, migration을 별도 계층으로 분리해 서비스 표면을 명확히 했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test` | `Tests 12 passed` | `SwaggerModule.setup("docs", app, swaggerDocument)` | 제출용 서비스는 기능 목록보다 bootstrap, docs, schema 표면이 먼저 읽힌다 | 인프라 제약을 service 경로 안에 넣어야 한다 |
| 2 | Phase 2 | Redis cache와 login throttling을 실제 정책으로 만든다 | `auth/auth-rate-limit.service.ts`, `auth/auth.service.ts`, `books/books.service.ts`, `runtime/redis.service.ts` | Redis는 controller 바깥에 얇게 붙여도 충분해 보였다 | login throttling, books cache, cache invalidation을 service flow 안으로 넣고 runtime config에 연결했다 | 같은 명령 재실행 | unit test 12개가 register/login/429/cache 관련 규칙을 통과한다 | `await this.authRateLimitService.ensureLoginAllowed(clientId)` | 인프라 의존성은 붙여 둔 장치가 아니라 실제 의사결정 경로를 바꾸는 제약이어야 한다 | infra 없는 상태의 실패도 검증해야 한다 |
| 3 | Phase 3 | Postgres/Redis를 포함한 실제 검증 루프를 돌린다 | `test/e2e/capstone.e2e.test.ts`, `docker-compose.yml` | unit test가 통과하면 제출용 검증도 거의 끝났다고 느끼기 쉽다 | infra 없이 e2e를 돌려 `ECONNREFUSED 127.0.0.1:5432`를 확인한 뒤, `docker compose up -d postgres redis` 후 e2e 16개를 전부 통과시켰다 | `pnpm run test:e2e` -> 실패, `docker compose up -d postgres redis`, `pnpm run test:e2e` -> 성공 | 첫 e2e는 `16 skipped`와 `connect ECONNREFUSED 127.0.0.1:5432`, 재실행은 `Tests 16 passed` | `await dataSource.runMigrations(); await seedDatabase(dataSource);` | shippable service의 검증은 앱 코드만이 아니라 필요한 인프라가 준비됐는지까지 포함한다 | 이 트랙의 마지막 단계다 |

## 근거 파일

- `applied/10-shippable-backend-service/README.md`
- `applied/10-shippable-backend-service/problem/README.md`
- `applied/10-shippable-backend-service/nestjs/src/app.bootstrap.ts`
- `applied/10-shippable-backend-service/nestjs/src/auth/auth.service.ts`
- `applied/10-shippable-backend-service/nestjs/src/auth/auth-rate-limit.service.ts`
- `applied/10-shippable-backend-service/nestjs/src/books/books.service.ts`
- `applied/10-shippable-backend-service/nestjs/src/runtime/redis.service.ts`
- `applied/10-shippable-backend-service/nestjs/src/database/migrations/1710000000000-initial-schema.ts`
- `applied/10-shippable-backend-service/nestjs/test/unit/auth.service.test.ts`
- `applied/10-shippable-backend-service/nestjs/test/e2e/capstone.e2e.test.ts`
- `applied/10-shippable-backend-service/docker-compose.yml`

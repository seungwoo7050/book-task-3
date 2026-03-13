# 10-shippable-backend-service series map

`10-shippable-backend-service`는 backend-node 트랙의 마지막 프로젝트다. 여기서 하는 일은 학습용 capstone을 더 복잡하게 만드는 게 아니라, Postgres, Redis, Swagger, Compose, migration, cache, throttling이 있는 제출용 surface로 다시 패키징하는 것이다. 그래서 이 시리즈는 "어떤 실행 계약을 새로 드러냈는가"라는 질문으로 읽는다.

## 복원 원칙

- chronology는 runtime config와 bootstrap을 먼저 세우고, Redis-backed 기능을 붙인 뒤, compose 기반 e2e로 닫는 순서로 복원한다.
- 근거는 `app.bootstrap.ts`, `runtime-config.ts`, `database-options.ts`, `books.service.ts`, `auth-rate-limit.service.ts`, `redis.service.ts`, `health.controller.ts`, `capstone.e2e.test.ts`, `docker-compose.yml`, 실제 CLI 출력이다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e   # infra 미기동 시 5432 연결 실패 확인
$ docker compose up -d postgres redis
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e   # 16 tests passed
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   runtime/infra surface, Redis-backed 운영 기능, compose-backed e2e 검증이 어떤 순서로 붙었는지 따라간다.

# 10-shippable-backend-service series map

이 프로젝트는 학습용 capstone을 그대로 끝내지 않고, Postgres, Redis, Swagger, Docker Compose까지 포함한 제출용 서비스 표면으로 다시 패키징한 단계다. 여기서의 질문은 "기능이 있느냐"보다 "실제 서비스처럼 읽히고, 실제 서비스처럼 검증되느냐"에 더 가깝다.

처음 읽을 때는 `app.bootstrap.ts`와 `auth.service.ts`, `books.service.ts`, 그리고 e2e 테스트를 한 줄로 보는 편이 좋다. bootstrap이 표면을 만들고, service가 Redis와 DB 같은 제약을 실제 정책으로 받아들이고, e2e가 인프라 준비 상태까지 포함해 그 표면을 검증하는 흐름이 자연스럽게 이어진다.

## 이 글에서 볼 것

- Swagger와 migration이 왜 제출용 표면의 일부가 되는지
- login throttling과 books cache가 service decision path 안으로 어떻게 들어오는지
- infra 없이 실패한 e2e와 compose 이후 성공한 e2e가 왜 둘 다 중요한 증거인지

## source of truth

- `applied/10-shippable-backend-service/README.md`
- `applied/10-shippable-backend-service/problem/README.md`
- `applied/10-shippable-backend-service/nestjs/src/app.bootstrap.ts`
- `applied/10-shippable-backend-service/nestjs/src/auth/*`
- `applied/10-shippable-backend-service/nestjs/src/books/books.service.ts`
- `applied/10-shippable-backend-service/nestjs/src/runtime/redis.service.ts`
- `applied/10-shippable-backend-service/nestjs/src/database/migrations/1710000000000-initial-schema.ts`
- `applied/10-shippable-backend-service/nestjs/test/unit/auth.service.test.ts`
- `applied/10-shippable-backend-service/nestjs/test/e2e/capstone.e2e.test.ts`
- `applied/10-shippable-backend-service/docker-compose.yml`

## 구현 흐름 한눈에 보기

1. `configureApp`와 migration으로 서비스 bootstrap과 schema 초기화를 분리한다.
2. Redis 기반 login throttling과 books cache/invalidation을 service 흐름 안으로 넣는다.
3. infra 없는 e2e 실패를 확인한 뒤 compose로 Postgres/Redis를 올려 16개 e2e를 통과시킨다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test
Tests       12 passed (12)
Duration    1.98s
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
FAIL: connect ECONNREFUSED 127.0.0.1:5432

$ docker compose up -d postgres redis
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  1 passed (1)
Tests       16 passed (16)
```

## 트랙의 끝에서

이 프로젝트는 `backend-node` 트랙의 마지막 장면이다. 이후 확장은 배포, worker, 외부 연동 같은 별도 포트폴리오 축으로 넘어간다.
